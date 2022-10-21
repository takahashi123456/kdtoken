import axios from "axios";
import { useState, useEffect } from 'react';
import React from "react";
class DjangoApi extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            error: null,
            isLoaded: false,
            items: []
        };
    }

    componentDidMount() {
        // fetch("http://192.168.3.106:8000/api/")
        fetch('https://jsonplaceholder.typicode.com/todos/1')
            .then(res => res.json())
            .then((result) => {
                    this.setState({
                        isLoaded: true,
                        items: result.items
                    });
                },
                // 補足：コンポーネント内のバグによる例外を隠蔽しないためにも
                // catch()ブロックの代わりにここでエラーハンドリングすることが重要です
                (error) => {
                    this.setState({
                        isLoaded: true,
                        error
                    });
                }
            )

    }

    render() {
        const { error, isLoaded, items } = this.state;
        console.log(this.state);
        if (error) {
            return <div>Error: {error.message}</div>;
        } else if (!isLoaded) {
            return <div>Loading...</div>;
        } else {
            return (
                <p>test</p>
                // <ul>
                //     {items.map(item => (
                //         <li key={item.id}>
                //             {/*{item.name} {item.price}*/}
                //         </li>
                //     ))}
                // </ul>
            );
        }
    }
}
export default DjangoApi;