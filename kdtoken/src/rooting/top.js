import React from 'react';
import Header from '../components/header/header';

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
            </div>
        </div>
    )
}