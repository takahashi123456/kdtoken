import React from 'react';
import Header from '../components/header/header';
import WeatherCheck from '../components/apiget';
import KeibaTB from '../components/body/table';
import KeibaTB9 from '../components/body/table';
import KeibaTB10 from '../components/body/table';
import Keiba12TB from '../components/body/table';
import { useState, useEffect } from 'react';
import Container from '@mui/material/Container';


const theme = {
    spacing: 8,
}

const sections = [
    { title: '過去の予想', url: '/list' },
    { title: '今週のレース予想', url: '#' },
    { title: 'モデル別回収率一覧', url: '#' },
    { title: 'お知らせ', url: '#' },
    { title: 'お問合せ', url: '#' },

];


export default function Top() {
    return (
        <div>
            <Header title="競馬AI" sections={sections} />
            <Container maxWidth="md">
                <KeibaTB />
                <WeatherCheck />
            </Container>
        </div >
    )
}