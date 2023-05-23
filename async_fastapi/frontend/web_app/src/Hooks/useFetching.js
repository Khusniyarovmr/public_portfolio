import { useState, useEffect } from 'react';
import axios from 'axios';

function useFetch(url) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        setLoading(true)
        setData(null);
        setError(null);
        const source = axios.CancelToken.source();
        axios.get(url, {cancelToken: source.token})
            .then(res => {
                setLoading(false);
                res.data.content && setData(res.data.content);
            })
            .catch(err => {
                setLoading(false)
                setError('An error occurred. Awkward..' + err.message)
            })
        return () => {
            source.cancel();
        }
    }, [url])

    return {data, loading, error}
}

export default useFetch;



// import useFetch from './useFetch';
// import './App.css';
//
// function App() {
//     const { data: quote, loading, error } = useFetch('https://api.quotable.io/random')
//
//     return (
//         <div className="App">
//             { loading && <p>{loading}</p> }
//             { quote && <p>"{quote}"</p> }
//             { error && <p>{error}</p> }
//         </div>
//     );
// }
//
// export default App;