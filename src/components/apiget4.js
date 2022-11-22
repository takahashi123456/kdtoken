import axios from "axios";
import React from "react";
import DenseTable from "./body/simple_table";
import DataTable_datail from "./body/simple_table_datail";



export default function Apitest4() {
    const baseURL = "http://192.168.1.140:8000/api/";

    const [ isLoading, setIsLoading ] = React.useState(false);
    const [posts, setPost] = React.useState(null);

    React.useEffect(() => {
        axios.get(baseURL).then((response) => {
            setPost(response.data);
            setIsLoading(true)
        }).catch(error => {
            console.log(error);
            setIsLoading(false);
        });
    }, []);

    if (!posts) return null;


    if (!isLoading) {
        return <div>Loading...</div>;
        }
    else {
        return (
            <>
            {posts.map(post => {
                // console.log(post);
                var Json_race =""
                if (Json_race == ""){
                Json_race = JSON.parse(post.score);
                }else{
                    console.log(Json_race);
                };
                return(
                <div key={post.race_id}>
                    <h1>レースID {post.race_id}</h1>
                    {/*<p>name {Json_race.horse_name[0]}</p>*/}
                    <DataTable_datail json={Json_race}  />
                </div>)
        })}
            </>
        )
    };
}