import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Data from '../../prediction.json';


const name = Data.horsename;
const score = Data.Score;
const favorite = Data.favorite;
const horsenumber = Data.horsenumber;
const age = Data.age;
const track = Data["track surface"]
const jockey = Data["jockey"]


function createData(name, jockey, calories, fat, carbs, protein, track) {
    return { name, jockey, calories, fat, carbs, protein, track };
}
const rows = [];
for (let i = 0; i < 9; i++) {
    const a = createData(name[i], jockey[i], score[i], favorite[i], horsenumber[i], age[i], track[i]);
    rows.push(a)
}
export default function KeibaTB() {
    return (
        <TableContainer component={Paper} className="mb-16">
            <Table sx={{ maxWidth: 1000 }} aria-label="simple table">
                <TableHead>
                    <TableRow>
                        <TableCell>ウマ名</TableCell>
                        <TableCell align="right">Score</TableCell>
                        <TableCell align="right">騎手</TableCell>
                        <TableCell align="right">馬人気</TableCell>
                        <TableCell align="right">ホースナンバー</TableCell>
                        <TableCell align="right">うま年齢</TableCell>
                        <TableCell align="right">トラック</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {rows.map((row) => (
                        <TableRow
                            key={row.name}
                            sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                        >
                            <TableCell component="th" scope="row">
                                {row.name}
                            </TableCell>
                            <TableCell align="right">{row.calories}</TableCell>
                            <TableCell align="right">{row.jockey}</TableCell>
                            <TableCell align="right">{row.fat}</TableCell>
                            <TableCell align="right">{row.carbs}</TableCell>
                            <TableCell align="right">{row.protein}</TableCell>
                            <TableCell align="right">{row.track}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
}
