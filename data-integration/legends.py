import json
import uuid

import pandas as pd
import sqlalchemy

LEGENDS_UUID = (uuid.uuid4(),)
LEGENDS = {
    "Protection level": {
        "vis_id": LEGENDS_UUID,
        "legend": {
            "name": "Protection level",
            "type": "custom",
            "symbology": [
                {
                    "red": 41,
                    "green": 55,
                    "blue": 144,
                    "opacity": 1,
                    "value": "1",
                    "label": "Protection forte",
                },
                {
                    "red": 61,
                    "green": 115,
                    "blue": 158,
                    "opacity": 1,
                    "value": "2",
                    "label": "Protection moyenne",
                },
                {
                    "red": 82,
                    "green": 176,
                    "blue": 172,
                    "opacity": 1,
                    "value": "3",
                    "label": "Protection limitée",
                },
                {
                    "red": 102,
                    "green": 235,
                    "blue": 186,
                    "opacity": 1,
                    "value": "4",
                    "label": "Pas de protection partimoniale",
                },
                {
                    "red": 177,
                    "green": 177,
                    "blue": 177,
                    "opacity": 1,
                    "value": "5",
                    "label": "Non concerné",
                },
            ],
        },
    }
}

legends = []
for key in LEGENDS.keys():
    legends.append(
        (
            LEGENDS[key]["vis_id"],
            json.dumps(LEGENDS[key]["legend"]),
        )
    )
legends_df = pd.DataFrame(legends, columns=["vis_id", "legend"])


def post_legend(
    engine: sqlalchemy.engine.Engine,
    legends: pd.DataFrame = legends_df,
    **kwargs,
) -> None:
    legends.to_sql(
        "visualization",
        engine,
        if_exists="append",
        index=False,
        **kwargs,
    )
