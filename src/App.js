import React from 'react';
import Header from './components/header/header';
import WeatherCheck from './components/apiget';
import KeibaTB from './components/body/table';
import { useState, useEffect } from 'react';
import Container from '@mui/material/Container';
const theme = {
  spacing: 8,
}

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
      <Container maxWidth="md">
        <h1>有馬記念</h1>
        <KeibaTB container />
        <WeatherCheck />
      </Container>
    </div >
  )
}