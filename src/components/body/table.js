import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Data from '../../data_predict_202207050210.json';
import Data2 from '../../data_predict_202207050209.json';
import Data3 from '../../data_predict_202207050211_CentaurS.json';
import Data4 from '../../data_predict_202207050212.json';


const name = Data["horse_name"];
const score = Data["Score"];
const favorite = Data["favorite"];
const horsenumber = Data["horse_number"];
const age = Data["age"];
const track = Data["track_surface"]
const jockey = Data["jockey"]
const label = Data["Label"]

const a_name = Data2["horse_name"];
const a_score = Data2["Score"];
const a_favorite = Data2["favorite"];
const a_horsenumber = Data2["horse_number"];
const a_age = Data2["age"];
const a_track = Data2["track_surface"]
const a_jockey = Data2["jockey"]
const a_label = Data["Label"]


const b_name = Data3["horse_name"];
const b_score = Data3["Score"];
const b_favorite = Data3["favorite"];
const b_horsenumber = Data3["horse_number"];
const b_age = Data3["age"];
const b_track = Data3["track_surface"]
const b_jockey = Data3["jockey"]
const b_label = Data["Label"]

const c_name = Data4["horse_name"];
const c_score = Data4["Score"];
const c_favorite = Data4["favorite"];
const c_horsenumber = Data4["horse_number"];
const c_age = Data4["age"];
const c_track = Data4["track_surface"]
const c_jockey = Data4["jockey"]
const c_label = Data4["Label"]

function createData(name, jockey, calories, fat, carbs, protein, track, label) {
    return { name, jockey, calories, fat, carbs, protein, track, label };
}
//後でForで簡単にみやすくする
const rows = [];
for (let i = 0; i < 16; i++) {
    const a = createData(name[i], jockey[i], score[i], favorite[i], horsenumber[i], age[i], track[i], label[i]);
    rows.push(a)
}

const rows2 = [];
for (let i = 0; i < 8; i++) {
    const a = createData(a_name[i], a_jockey[i], a_score[i], a_favorite[i], a_horsenumber[i], a_age[i], a_track[i], a_label[i]);
    rows2.push(a)
}
const rows3 = [];
for (let i = 0; i < 13; i++) {
    const a = createData(b_name[i], b_jockey[i], b_score[i], b_favorite[i], b_horsenumber[i], b_age[i], b_track[i], b_label[i]);
    rows3.push(a)
}
const rows4 = [];
for (let i = 0; i < 12; i++) {
    const a = createData(c_name[i], c_jockey[i], c_score[i], c_favorite[i], c_horsenumber[i], c_age[i], c_track[i], c_label[i]);
    rows4.push(a)
}

export default function KeibaTB() {
    return (
        <>
            <h1>9R長久手特別 </h1>
            <TableContainer component={Paper} className="mb-16">
                <Table sx={{ maxWidth: 1000 }} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell>ウマ名</TableCell>
                            <TableCell align="right">Score</TableCell>
                            <TableCell align="right">着予想(1なら３着以内という意味)</TableCell>
                            <TableCell align="right">騎手</TableCell>
                            <TableCell align="right">馬人気</TableCell>
                            <TableCell align="right">ホースナンバー</TableCell>
                            <TableCell align="right">うま年齢</TableCell>
                            <TableCell align="right">トラック</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {rows2.map((row1) => (
                            <TableRow
                                key={row1.name}
                                sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                            >
                                <TableCell component="th" scope="row">
                                    {row1.name}
                                </TableCell>
                                <TableCell align="right">{row1.calories}</TableCell>
                                <TableCell align="right">{row1.label}</TableCell>
                                <TableCell align="right">{row1.jockey}</TableCell>
                                <TableCell align="right">{row1.fat}</TableCell>
                                <TableCell align="right">{row1.carbs}</TableCell>
                                <TableCell align="right">{row1.protein}</TableCell>
                                <TableCell align="right">{row1.track}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
            <h1>10R 浜松S</h1>
            <TableContainer component={Paper} className="mb-16">
                <Table sx={{ maxWidth: 1000 }} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell>ウマ名</TableCell>
                            <TableCell align="right">Score</TableCell>
                            <TableCell align="right">着予想(1なら３着以内という意味)</TableCell>
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
                                <TableCell align="right">{row.label}</TableCell>
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
            <h1>11R セントウルステークス</h1>
            <TableContainer component={Paper} className="mb-16">
                <Table sx={{ maxWidth: 1000 }} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell>ウマ名</TableCell>
                            <TableCell align="right">Score</TableCell>
                            <TableCell align="right">着予想(1なら３着以内という意味)</TableCell>
                            <TableCell align="right">騎手</TableCell>
                            <TableCell align="right">馬人気</TableCell>
                            <TableCell align="right">ホースナンバー</TableCell>
                            <TableCell align="right">うま年齢</TableCell>
                            <TableCell align="right">トラック</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {rows3.map((row3) => (
                            <TableRow
                                key={row3.name}
                                sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                            >
                                <TableCell component="th" scope="row">
                                    {row3.name}
                                </TableCell>
                                <TableCell align="right">{row3.calories}</TableCell>
                                <TableCell align="right">{row3.label}</TableCell>
                                <TableCell align="right">{row3.jockey}</TableCell>
                                <TableCell align="right">{row3.fat}</TableCell>
                                <TableCell align="right">{row3.carbs}</TableCell>
                                <TableCell align="right">{row3.protein}</TableCell>
                                <TableCell align="right">{row3.track}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
            <h1>12R 3歳以上1勝クラス</h1>
            <TableContainer component={Paper} className="mb-16">
                <Table sx={{ maxWidth: 1000 }} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell>ウマ名</TableCell>
                            <TableCell align="right">Score</TableCell>
                            <TableCell align="right">着予想(1なら３着以内という意味)</TableCell>
                            <TableCell align="right">騎手</TableCell>
                            <TableCell align="right">馬人気</TableCell>
                            <TableCell align="right">ホースナンバー</TableCell>
                            <TableCell align="right">うま年齢</TableCell>
                            <TableCell align="right">トラック</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {rows4.map((row4) => (
                            <TableRow
                                key={row4.name}
                                sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                            >
                                <TableCell component="th" scope="row">
                                    {row4.name}
                                </TableCell>
                                <TableCell align="right">{row4.calories}</TableCell>
                                <TableCell align="right">{row4.label}</TableCell>
                                <TableCell align="right">{row4.jockey}</TableCell>
                                <TableCell align="right">{row4.fat}</TableCell>
                                <TableCell align="right">{row4.carbs}</TableCell>
                                <TableCell align="right">{row4.protein}</TableCell>
                                <TableCell align="right">{row4.track}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>

        </>
    );
}
