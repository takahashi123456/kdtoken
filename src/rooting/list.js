import React from 'react';
import DjangoApi from '../components/apiget2';
import Header from "../components/header/header";
import Apitest4 from "../components/apiget4";
import Container from '@mui/material/Container';


const sections = [
    { title: '今週の予想', url: '/list' },
    { title: '最強馬レート', url: '/rate' },
    { title: 'モデル別回収率一覧', url: '#' },
    { title: 'お知らせ', url: '#' },
    { title: 'お問合せ', url: '/contact' },
];


export default class List extends React.Component {
    render() {
        return (
            <div>
                <Header title="競馬AI" sections={sections} />
                <Container>
                    <h1>今週のレース結果表示</h1>
                    <Apitest4 />
                </Container>
            </div>
        )
    }
}