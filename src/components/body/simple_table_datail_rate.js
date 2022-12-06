import * as React from 'react';
import { DataGrid } from '@mui/x-data-grid';

function createData(id, horse_name, uma, rate) {
    return { id, horse_name, uma, rate };
}

const columns = [
    { field: 'id', headerName: 'id', width: 150 },
    { field: 'horse_name', headerName: 'horse_name', width: 150 },
    { field: 'uma', headerName: '馬名（日本語)', width: 150 },
    { field: 'rate', headerName: '馬レート', type: 'number', width: 200 },
];

export default function Simple_table_datail_rate(props) {
    const rows = []
    const json = props.json
    console.log(json[0].horse_name)
    const a = "rate"
    const race_length = json.length;
    console.log(race_length)
    for (let i = 0; i < race_length; i++) {
        const horse_info = createData(i, json[i]["horse_name"], json[i]["uma_name"], json[i]["rate"])
        rows.push(horse_info)
    }
    return (
        <div style={{ height: "100%", width: '57%', alignItems: "center", margin: "auto" }}>
            <DataGrid
                rows={rows}
                columns={columns}
                pageSize={race_length}
                autoHeight="True"
                disableExtendRowFullWidth="True"
            />
        </div>
    );
}