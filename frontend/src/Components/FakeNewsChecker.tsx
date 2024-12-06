// src/FakeNewsChecker.tsx
import React, { useState } from 'react';
import axios from 'axios';
import bg from '/bg.jpg';
// import '/bg.jpg';

import "./FakeNewsChecker.css";

const FakeNewsChecker: React.FC = () => {
    const [article, setArticle] = useState<string>('');
    const [result, setResult] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string>('');

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        setResult('');

        try {
            const response = await axios.post<{ result: string }>('/api/check-article', { article });
            setResult(response.data.result);
        } catch (err) {
            setError('Error checking the article. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className='home' style={{backgroundSize: 'cover',backgroundRepeat: 'no-repeat'}}>
            <h1>Fake News Checker</h1>
            <form onSubmit={handleSubmit}>
                {/* <textarea
                    value={article}
                    onChange={(e) => setArticle(e.target.value)}
                    placeholder="Paste your article here"
                    rows={10}
                    cols={50}
                    required
                /> */}
                {/* INPUT ARTICLE */}
                <input type="text"  placeholder="Paste your article here" onChange={(e) => setArticle(e.target.value)}></input>
                &ensp;
                <button type="submit" disabled={loading}>
                    {loading ? 'Checking...' : 'Check Article'}
                </button>
            </form>
            {result && <p>Result: {result}</p>}
            {error && <p style={{ color: 'red' }}>{error}</p>}
        </div>
    );
};

export default FakeNewsChecker;