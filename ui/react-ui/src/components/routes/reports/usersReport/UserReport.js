import React, { useState, useEffect } from 'react';
import { JsonToTable } from "react-json-to-table";

function UserReport() {
    const [jsonReport, setJsonReport] = useState();
    const [showJson, setshowJson] = useState(false);
    const jsonUrl = "https://nate-temp-bucket.s3-us-west-2.amazonaws.com/report_users_user_id_tasks_task_id.json";
    
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
        <div className="userReportTable">
            <h1>/users/ Serverless-Artillery Report</h1>
            <button
            onClick={() => setshowJson(!showJson)}>Show {toggleJson}</button>
            {showJson ? <div><pre>{ JSON.stringify(jsonReport, null, 2) }</pre></div> : <JsonToTable json={jsonReport}/>}
        </div>
    );
}

export default UserReport;