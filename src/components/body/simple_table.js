import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

function createData(horse_number, horse_name, jockey, horse_weight, favorite, odds,deviationValue) {
    return {horse_number, horse_name, jockey, horse_weight, favorite, odds,deviationValue };
}

// const rows = [
//     createData('Frozen yoghurt', 159, 6.0, 24, 4.0),
//     createData('Ice cream sandwich', 237, 9.0, 37, 4.3),
//     createData('Eclair', 262, 16.0, 24, 6.0),
//     createData('Cupcake', 305, 3.7, 67, 4.3),
//     createData('Gingerbread', 356, 16.0, 49, 3.9),
// ];

export default function DenseTable(props) {
    const rows = []
    const json = props.json
    const race_length = Object.keys(json["horse_name"]).length;
    for (let i = 0; i < race_length; i++){
        const horse_info = createData(json.horse_number[i],json.horse_name[i],json.jockey[i],json.horse_weight[i],json.favorite[i],json.odds[i],json.DeviationValue[i])
        rows.push(horse_info)
    }
    return (
        <TableContainer component={Paper}>
            <Table sx={{ minWidth: 650 }} size="small" aria-label="a dense table">
                <TableHead>
                    <TableRow>
                        <TableCell>馬番</TableCell>
                        <TableCell>ウマ名</TableCell>
                        <TableCell align="right">騎手</TableCell>
                        <TableCell align="right">馬体重</TableCell>
                        <TableCell align="right">人気</TableCell>
                        <TableCell align="right">オッズ</TableCell>
                        <TableCell align="right">強さ偏差値</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {rows.map((row) => (
                        <TableRow
                            key={row.horse_number}
                            sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                        >
                            <TableCell component="th" scope="row">{row.horse_number}</TableCell>
                            <TableCell component="th" scope="row">{row.horse_name}</TableCell>
                            <TableCell align="right">{row.jockey}</TableCell>
                            <TableCell align="right">{row.horse_weight}</TableCell>
                            <TableCell align="right">{row.favorite}</TableCell>
                            <TableCell align="right">{row.odds}</TableCell>
                            <TableCell align="right">{row.deviationValue}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
}