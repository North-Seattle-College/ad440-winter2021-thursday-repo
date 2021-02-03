
import React, { useState, useEffect } from 'react';
import { JsonToTable } from "react-json-to-table";

function TasksReport() {
    const [jsonReport, setJsonReport] = useState('');
    const jsonUrl = "https://luca-artillery-report.s3-us-west-2.amazonaws.com/report__for_30req.json";
    const proxy  = 'https://cors-anywhere.herokuapp.com/';

    const grabReport = async () => {
        const response = await fetch(proxy +jsonUrl)
        const json = await response.json();
        setJsonReport(json);
    }

    useEffect(() => {
        if (!jsonReport) grabReport();
    }, [jsonReport])

    return (
        <div className="TaskIdReportTable">
            <h1>/users/{'{'}user_id{'}'}/tasks Serverless-Artillery Report</h1>
            <JsonToTable json={jsonReport}/>
        </div>
    );
}

export default TasksReport; 