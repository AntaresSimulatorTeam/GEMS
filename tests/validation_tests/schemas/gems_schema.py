from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class PortField(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str


class PortType(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str
    description: Optional[str] = None
    fields: list[PortField] = Field(default_factory=list)


class Port(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str
    type: str


class Parameter(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str


class Variable(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str


class ModelDefinition(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str
    parameters: list[Parameter] = Field(default_factory=list)
    variables: list[Variable] = Field(default_factory=list)
    ports: list[Port] = Field(default_factory=list)


class Library(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str
    description: Optional[str] = None
    port_types: list[PortType] = Field(default_factory=list, alias="port-types")
    models: list[ModelDefinition] = Field(default_factory=list)


class LibraryFile(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    library: Library


class ComponentParameter(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str
    value: Any = None


class Component(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str
    model: str
    parameters: list[ComponentParameter] = Field(default_factory=list)


class Connection(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    component1: str
    component2: str
    port1: str
    port2: str


class System(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str
    components: list[Component] = Field(default_factory=list)
    connections: list[Connection] = Field(default_factory=list)


class SystemFile(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    system: System
