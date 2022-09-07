import React from 'react';
import Header from '../components/header/header';
import WeatherCheck from '../components/apiget';
import BasicTable from '../components/body/table';
import { useState, useEffect } from 'react';


const sections = [
    { title: '過去の予想', url: '#' },
    { title: 'モデル別回収率一覧', url: '#' },
    { title: '今週のレース予想', url: '#' },
    { title: 'お知らせ', url: '#' },
    { title: 'お問合せ', url: '#' },

];


export default function Top() {
    return (
        <div>
            <Header title="競馬AI" sections={sections} />
            <div>
                <h1>Hello, world!</h1>
                <WeatherCheck />
                <BasicTable />
            </div>
        </div>
    )
}