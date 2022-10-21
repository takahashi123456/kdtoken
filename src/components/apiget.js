import axios from "axios";
import { useState, useEffect } from 'react';

const WeatherCheck = () => {
    const apikey = "8de599331517de1e3fd79d0b88951090"

    const baseURL = `https://api.openweathermap.org/data/2.5/weather?q=Osaka,JPforecast?id=524901&appid=${apikey}&units=metric`;
    const URL = "http://192.168.1.186:8000/api/1"
    const [post, setPost] = useState(null);
    useEffect(() => {
        axios.get(baseURL).then((response) => {
            setPost(response.data);
        });
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);
    // eslint-disable-next-line react-hooks/exhaustive-deps

    if (!post) return null;
    const { weather, main, name } = post;
    console.log(post);

    return (
        <div className="mb-16">
            <h2 className="text-xl mb-6">仮APIとしてopenWetherAPI</h2>
            <p className="mb-4">空模様 : {weather[0].description}</p>
            <p>気温 : {main.temp}</p>
            <p>Osaka : {name} </p>
        </div>
    );
}
export default WeatherCheck;