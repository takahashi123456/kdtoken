import axios from "axios";
import React from "react";

const baseURL = "https://jsonplaceholder.typicode.com/todos/1";

export default function Apitest3() {
    const [ isLoading, setIsLoading ] = React.useState(false);
    const [post, setPost] = React.useState(null);

    React.useEffect(() => {
        axios.get(baseURL).then((response) => {
            setPost(response.data);
            setIsLoading(true)
        }).catch(error => {
            console.log(error);
            setIsLoading(false);
        });
    }, []);

    if (!post) return null;

    if (!isLoading) {
        return <div>Loading...</div>;
        }
    else {
        return (
            <div>
                <h1>レースID {post.id}</h1>
                <p>テスト {post.title}</p>
            </div>)
    };
}