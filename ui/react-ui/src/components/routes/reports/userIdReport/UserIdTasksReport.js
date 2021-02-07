
import React, { useState, useEffect } from 'react';
import { JsonToTable } from "react-json-to-table";

function TasksReport() {
    const [jsonReport, setJsonReport] = useState('');
    const jsonUrl = "https://nate-temp-bucket.s3-us-west-2.amazonaws.com/report_users_user_id_tasks_task_id.json";
   // const proxy  = 'https://cors-anywhere.herokuapp.com/'; proxy +

    const grabReport = async () => {
        const response = await fetch(jsonUrl)
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