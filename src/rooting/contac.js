import React from 'react';
import DjangoApi from '../components/apiget2';
import Header from "../components/header/header";
import Apitest3 from "../components/apiget3";
import Container from '@mui/material/Container';
import Form from "../components/body/form";


const sections = [
    { title: '過去の予想', url: '/list' },
    { title: '今週のレース予想', url: '#' },
    { title: 'モデル別回収率一覧', url: '#' },
    { title: 'お知らせ', url: '#' },
    { title: 'お問合せ', url: '/contact' },
];


export default class Contact extends React.Component {
    render() {
        return (
            <div>
                <Header title="競馬AI" sections={sections} />
                <Container>
                    <h1>お問合せ</h1>
                    <Form />
                </Container>
            </div>
        )
    }
}