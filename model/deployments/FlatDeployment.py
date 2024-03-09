from dataclasses import dataclass, field

from model.props.ConfigProp import ConfigProp


@dataclass
class FlatDeployment:
    id: int = field()
    priority: int = field()
    props: list[ConfigProp] = field(default_factory=list)
