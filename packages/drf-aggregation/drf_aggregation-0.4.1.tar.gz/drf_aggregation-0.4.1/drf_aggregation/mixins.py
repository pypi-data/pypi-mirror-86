import json

from django.db import models
from drf_complex_filter.utils import generate_query_from_dict
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .aggregates import CountIf
from .aggregates import Percentile
from .utils import Aggregator


class AggregationMixin:
    def aggregation(self, request):
        aggregation = self._get_aggregation(request)
        annotations = self._get_annotation(aggregation=aggregation,
                                           request=request)
        queryset = self.filter_queryset(self.get_queryset())

        limit = self._get_limit(request=request)
        limit_field = self._get_limit_by_field(request=request)
        if limit and not limit_field:
            raise ValidationError(
                {"error": "limitByField is required if a limit is set."})

        aggregator = Aggregator(queryset=queryset)
        result = aggregator.get_database_aggregation(
            annotations=annotations,
            group_by=self._get_group_by(request=request),
            limit=self._get_limit(request=request),
            limit_field=self._get_limit_by_field(request=request),
            order=self._get_order(request=request),
            show_other=self._get_show_other(request=request),
            other_group_name=self._get_other_group_name(request=request))

        return Response(result)

    def _get_annotation(self, aggregation: str, request) -> dict:
        if aggregation == 'count':
            return {"value": models.Count('id')}

        if aggregation == 'sum':
            aggregation_field = self._get_aggregation_field(request=request)
            return {"value": models.Sum(aggregation_field)}

        if aggregation == 'average':
            aggregation_field = self._get_aggregation_field(request=request)
            return {"value": models.Avg(aggregation_field)}

        if aggregation == 'minimum':
            aggregation_field = self._get_aggregation_field(request=request)
            return {"value": models.Min(aggregation_field)}

        if aggregation == 'maximum':
            aggregation_field = self._get_aggregation_field(request=request)
            return {"value": models.Max(aggregation_field)}

        if aggregation == 'percentile':
            aggregation_field = self._get_aggregation_field(request=request)
            percentile = self._get_percentile(request)
            output_type = self._get_output_type(request=request)
            if output_type == 'float':
                return {"value": Percentile(aggregation_field, percentile,
                                            output_field=models.FloatField())}
            return {"value": Percentile(aggregation_field, percentile)}

        if aggregation == "percent":
            additional_query = self._get_additional_query(request=request)
            return {
                "numerator": CountIf(additional_query),
                "denominator": models.Count("id"),
                "value": models.ExpressionWrapper(
                    models.F("numerator") * 1.0 / models.F("denominator"),
                    output_field=models.FloatField())
            }

        raise ValidationError({"error": "Unknown aggregation."})

    @staticmethod
    def _get_aggregation(request) -> str:
        aggregation = request.query_params.get("aggregation", None)
        if not aggregation:
            raise ValidationError({"error": "Aggregation is mandatory."})

        return aggregation

    @staticmethod
    def _get_group_by(request) -> list:
        group_by = request.query_params.get("groupByFields", None)
        group_by = group_by.split(",") if group_by else []

        return group_by

    @staticmethod
    def _get_order(request) -> (str, None):
        return request.query_params.get("order", None)

    @staticmethod
    def _get_limit(request) -> (int, None):
        limit = request.query_params.get("limit", None)
        return int(limit) if limit else None

    @staticmethod
    def _get_limit_by_field(request) -> (str, None):
        return request.query_params.get("limitByField", None)

    @staticmethod
    def _get_show_other(request) -> bool:
        show_other = request.query_params.get("showOther", None)
        return show_other == "1"

    @staticmethod
    def _get_other_group_name(request) -> str:
        return request.query_params.get("otherGroupName", None)

    @staticmethod
    def _get_aggregation_field(request) -> str:
        aggregation_field = request.query_params.get("aggregationField", None)
        if not aggregation_field:
            raise ValidationError({"error": "Aggregation field is mandatory."})

        return aggregation_field

    @staticmethod
    def _get_additional_query(request) -> models.Q:
        try:
            additional_filter = json.loads(
                request.query_params.get("additionalFilter", None)
            )
        except (TypeError, json.decoder.JSONDecodeError):
            raise ValidationError({"error": "Additional filter is mandatory."})
        additional_query = generate_query_from_dict(additional_filter)
        if not additional_query:
            raise ValidationError(
                {"error": "Additional filter cannot be empty."}
            )

        return additional_query

    @staticmethod
    def _get_percentile(request) -> str:
        percentile = request.query_params.get("percentile", None)
        if not percentile:
            raise ValidationError({"error": "Percentile is mandatory."})

        return percentile

    @staticmethod
    def _get_output_type(request) -> (str, None):
        return request.query_params.get("outputType", None)
