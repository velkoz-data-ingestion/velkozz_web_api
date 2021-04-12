// Daily Indexs:
const daily_get_timeseries = JSON.parse(document.getElementById('get_datetime').textContent);
//const daily_post_timeseries = JSON.parse(document.getElementById('post_datetime').textContent);

// Daily Request Counts:
const daily_get_request_count = JSON.parse(document.getElementById("get_requests_count").textContent);
const daily_post_request_count = JSON.parse(document.getElementById("post_requests_count").textContent);

// Creating the GET and POST daily requests summary timeseries data:
const daily_GET_summary_trace = {
    type: "scatter",
    name: "GET Requests",
    fill: 'tozeroy', 
    stackgroup: 'one',
    x: Date(...daily_get_timeseries),
    y: daily_get_request_count
};

const daily_POST_summary_trace = {
    type: "scatter",
    name: "POST Requests",
    fill: 'tozeroy', 
    stackgroup: 'one',
    x: Date(...daily_get_timeseries),
    y: daily_post_request_count
};

// Building Summary Request Area Chart Traces: 
const request_summary_data = [daily_GET_summary_trace, daily_POST_summary_trace];

// Creating the ScatterPlot for daily request summaries: 
Plotly.newPlot("summary_request_timeseries", request_summary_data, {
    
    height: 500,
    title: "Summary of Requests Made to the Server",
    plot_bgcolor: "rgba(0,0,0,0)",
    paper_bgcolor: "rgba(0,0,0,0)",
    
    font: {
        color: "#b2becd"
    }, 
    
    // Axis Title Formatting:
    xaxis: {
        title: "Local Time (UTC-4)",
        type: 'date',
        tickformat: '%Y-%m-%j-%H:%M',
        nticks: 10,
        gridcolor: "#b2becd"
    },

    yaxis: {
        title: "HTTP Requests",
        gridcolor: "#b2becd"
    }


});