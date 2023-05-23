import React from "react";
import Loader from 'react-loader';
import useFetch from "../../Hooks/useFetching";


export default function Timing() {
    const {loading} = useFetch('/timing')


    return (
        <section>
            {
                loading ? <Loader/> : <h1>DONE</h1>
            }
        </section>
    )
}