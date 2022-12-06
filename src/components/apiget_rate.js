import axios from "axios";
import React from "react";
import DenseTable from "./body/simple_table";
import Simple_table_datail_rate from "./body/simple_table_datail_rate";
import Horse_rating from './horse_rating.json';



export default function Apitest5() {

    {
        const path = "/Users/hasebe/Desktop/team_lec/kdtoken/kdtoken/src/components/horse_rating.json"
        return (
            <>
                {/*<p>name {Json_race.horse_name[0]}</p>*/}
                < Simple_table_datail_rate json={Horse_rating} />
            </>
        )
    };
}