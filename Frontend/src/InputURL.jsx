import React, { useState } from "react";

const InputURL = ({ onEvaluate, isLoading }) => {
    const [input, setInput] = useState("");

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!input.trim()) return;
        onEvaluate(input);
    };

    return (
        <form className="input-url-form" onSubmit={handleSubmit}>
            <input
                type="text"
                placeholder="İlan URL'ini buraya girin"
                value={input}
                onChange={e => setInput(e.target.value)}
                disabled={isLoading}
                className="input-url"
            />
            <button type="submit" className="evaluate-btn" disabled={isLoading}>
                {isLoading ? (
                    <span className="spinner" aria-label="loading"></span>
                ) : (
                    "Değerlendir"
                )}
            </button>
        </form>
    );
};

export default InputURL;
