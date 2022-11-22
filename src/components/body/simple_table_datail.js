import * as React from 'react';
import { DataGrid } from '@mui/x-data-grid';

function createData(id, horse_name, jockey, horse_weight, favorite, odds,deviationValue) {
    return {id, horse_name, jockey, horse_weight, favorite, odds,deviationValue };
}

const columns = [
    { field: 'id', headerName: 'id', width: 100 },
    { field: 'horse_name', headerName: 'horse_name', width: 150 },
    { field: 'jockey', headerName: 'jockey', width: 150 },
    { field: 'horse_weight', headerName: 'horse_weight', type: 'number', width: 200},
    { field: 'favorite', headerName: 'favorite', type: 'number', width: 150},
    { field: 'odds', headerName: 'odds', type: 'number', width: 150},
    { field: 'deviationValue', headerName: '勝率偏差値', type: 'number', width: 200}
];

export default function DataTable_datail(props) {
    console.log(props)
    const rows = []
    const json = props.json
    const race_length = Object.keys(json["horse_name"]).length;
    for (let i = 0; i < race_length; i++){
        const horse_info = createData(json.horse_number[i],json.horse_name[i],json.jockey[i],json.horse_weight[i],json.favorite[i],json.odds[i],json.DeviationValue[i])
        rows.push(horse_info)
    }
    return (
        <div style={{ height: "100%", width: '98%' }}>
            <DataGrid
                rows={rows}
                columns={columns}
                pageSize={race_length}
                rowsPerPageOptions={[7]}
                autoHeight="True"
                disableExtendRowFullWidth="True"
            />
        </div>
    );
}