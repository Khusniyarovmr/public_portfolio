import { useState, useEffect } from 'react';
import axios from 'axios';

function usePosting(url, data, config={}) {
    const [status, setStatus] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        setLoading(true)
        setStatus(null);
        setError(null);
        axios.post(url, data, config)
            .then(res => {
                setLoading(false);
                res.status && setStatus(res.status);
            })
            .catch(err => {
                setLoading(false)
                setError('An error occurred. Awkward..' + err.message)
            });
    }, [url])

    return {status, loading, error}
}

export default usePosting;