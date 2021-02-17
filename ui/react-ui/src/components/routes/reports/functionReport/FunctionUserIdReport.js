import React, { useState, useEffect } from 'react';
import { JsonToTable } from "react-json-to-table";
import {useParams} from "react-router-dom";

function FunctionUserIdReport() {
    const [jsonReport, setJsonReport] = useState();
    const [showJson, setshowJson] = useState(false);
    var {userId} = useParams();
    const jsonUrl = `https://nsc-fun-dev-usw2-thursday.azurewebsites.net/api/users/${userId}?`;
    
    
    
    const getReport = async () => {
        const response = await fetch(jsonUrl)
        const json = await response.json();
        setJsonReport(json);
    }

    const toggleJson = showJson ? 'Table' : 'JSON';

    useEffect(() => {
        if (!jsonReport) getReport();
    }, [jsonReport])

    return (
        <div className="userIdRportTable">
            <h1>/users/{'{'}user_id{'}'} Azure Function Report</h1>
            <button
            onClick={() => setshowJson(!showJson)}>Show {toggleJson}</button>
            {showJson ? <div><pre>{ JSON.stringify(jsonReport, null, 2) }</pre></div> : <JsonToTable json={jsonReport}/>}
        </div>
    );
}

export default FunctionUserIdReport;