from typing import Union, List, Optional, Generic, TypeVar

from pyspark.sql import Column, DataFrame
from pyspark.sql.functions import array
from pyspark.sql.functions import lit

from spark_auto_mapper.data_types.data_type_base import AutoMapperDataTypeBase
from spark_auto_mapper.helpers.spark_higher_order_functions import filter
from spark_auto_mapper.helpers.value_parser import AutoMapperValueParser
from spark_auto_mapper.type_definitions.native_types import AutoMapperNativeSimpleType

_T = TypeVar(
    "_T", bound=Union[AutoMapperNativeSimpleType, AutoMapperDataTypeBase]
)


class AutoMapperList(AutoMapperDataTypeBase, Generic[_T]):
    """
    Base class for lists
    Generics:  https://mypy.readthedocs.io/en/stable/generics.html
    Multiple Inheritance:
    https://stackoverflow.com/questions/52754339/how-to-express-multiple-inheritance-in-python-type-hint
    """
    def __init__(
        self,
        value: Optional[List[_T]],
        remove_nulls: bool = True,
        include_null_properties: bool = False
    ) -> None:
        """
        Generates a list (array) in Spark

        :param value: items to make into an array
        :param remove_nulls: whether to remove nulls from the array
        """
        super().__init__()
        # can a single mapper or a list of mappers
        self.remove_nulls: bool = remove_nulls
        self.value: Union[AutoMapperDataTypeBase, List[AutoMapperDataTypeBase]]
        if not value:
            self.value = []
        if isinstance(value, str):
            self.value = AutoMapperValueParser.parse_value(value=value)
        elif isinstance(value, AutoMapperDataTypeBase):
            self.value = value
        elif isinstance(value, List):
            if include_null_properties and len(
                value
            ) > 1:  # if there are multiple items and the structs don't match then Spark errors
                self.value = [
                    AutoMapperValueParser.parse_value(v, include_nulls=True)
                    for v in value
                ]
            else:
                self.value = [
                    AutoMapperValueParser.parse_value(v) for v in value
                ]
        else:
            raise ValueError(f"{type(value)} is not supported")

    def get_column_spec(self, source_df: DataFrame) -> Column:
        if isinstance(
            self.value, str
        ):  # if the src column is just string then consider it a sql expression
            return array(lit(self.value))

        if isinstance(
            self.value, list
        ):  # if the src column is a list then iterate
            return filter(array(
                [
                    self.get_value(item, source_df=source_df)
                    for item in self.value
                ]
            ), lambda x: x.isNotNull()) \
                if self.remove_nulls \
                else array(
                [
                    self.get_value(item, source_df=source_df)
                    for item in self.value
                ]
            )

        # if value is an AutoMapper then ask it for its column spec
        if isinstance(self.value, AutoMapperDataTypeBase):
            child: AutoMapperDataTypeBase = self.value
            return filter(array(child.get_column_spec(source_df=source_df)), lambda x: x.isNotNull()) \
                if self.remove_nulls \
                else array(child.get_column_spec(source_df=source_df))

        raise ValueError(f"value: {self.value} is neither str nor AutoMapper")
