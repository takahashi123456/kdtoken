import axios from "axios";
import { useState, useEffect } from 'react';

const WeatherCheck = () => {
    const apikey = "8de599331517de1e3fd79d0b88951090"

    const baseURL = `http://api.openweathermap.org/data/2.5/weather?q=Osaka,JPforecast?id=524901&appid=${apikey}&units=metric`;

    const [post, setPost] = useState(null);
    useEffect(() => {
        axios.get(baseURL).then((response) => {
            setPost(response.data);
        });
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);
    if (!post) return null;
    const { weather, main, name } = post;
    console.log(post);

    return (
        <div className="mb-16">
            <h2 className="text-xl mb-6">東京の気象情報</h2>
            <p className="mb-4">空模様 : {weather[0].description}</p>
            <p>気温 : {main.temp}</p>
            <p>Osaka : {name} </p>
        </div>
    );
}
export default WeatherCheck;