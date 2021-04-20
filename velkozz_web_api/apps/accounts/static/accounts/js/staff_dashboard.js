// Daily Indexs:
const daily_get_timeseries = JSON.parse(document.getElementById('datetime').textContent);
//const daily_post_timeseries = JSON.parse(document.getElementById('post_datetime').textContent);

// Daily Request Counts:
const daily_get_request_count = JSON.parse(document.getElementById("get_requests_count").textContent);
const daily_post_request_count = JSON.parse(document.getElementById("post_requests_count").textContent);

// Data for App Specific Data:
const app_data = JSON.parse(document.getElementById("app_timeseries").textContent);

// Data for Response Codes:
const response_codes = JSON.parse(document.getElementById("response_codes").textContent);


// Creating the GET and POST daily requests summary timeseries data:
const main_date = daily_get_timeseries.map(date_str => Date.parse(date_str));

const daily_GET_summary_trace = {
    type: "scatter",
    name: "GET",
    fill: 'tozeroy', 
    stackgroup: 'one',
    x: main_date,
    y: daily_get_request_count
};

const daily_POST_summary_trace = {
    type: "scatter",
    name: "POST",
    fill: 'tozeroy', 
    stackgroup: 'one',
    x: main_date,
    y: daily_post_request_count
};

// Building Summary Request Area Chart Traces: 
const request_summary_data = [daily_GET_summary_trace, daily_POST_summary_trace];

// Creating the ScatterPlot for daily request summaries: 
Plotly.newPlot("summary_request_timeseries", request_summary_data, {
    
    height: 400,
    title: "Requests",
    margin: {
        t: 40
    },
    plot_bgcolor: "rgba(0,0,0,0)",
    paper_bgcolor: "rgba(0,0,0,0)",
    
    font: {
        color: "#b2becd"
    }, 
    
    // Axis Title Formatting:
    xaxis: {
        title: "Local Time (UTC-4)",
        type: 'date',
        tickformat: '%m-%d-%H:%M',
        nticks: 10,
        gridcolor: "#b2becd",
        linecolor: "#b2becd",
        linewidth: 1,
        mirror: true, 
        showgrid: false
    },

    yaxis: {
        title: "HTTP Requests",
        gridcolor: "#b2becd",
        linecolor: "#b2becd",
        linewidth: 2,
        mirror: true,
        showgrid: false
    }


});

// Manually creating data traces from app_data:
// TODO: Is there a way to do this dynamically? Does it make sense?

// Account App:
const account_requests = [{
    type: "scatter",
    name: "GET",
    fill: 'tozeroy', 
    stackgroup: 'one',
    marker: {
        color: '#32CD32'
      },    
    x: app_data['accounts']['GET']["Index"].map(date => Date.parse(date)),
    y: app_data['accounts']['GET']["Data"]
}, 
{
    type: "scatter",
    name: "POST",
    marker: {
        color: '#ff2a26'
      },    
    fill: 'tozeroy',    
    stackgroup: 'one',
    x: app_data['accounts']['POST']["Index"].map(date => Date.parse(date)),
    y: app_data['accounts']['POST']["Data"]
}];

Plotly.newPlot("account_request", account_requests, {    
    height: 350,
    margin: {
        t: 40
    },
    title: "Account App",
    plot_bgcolor: "rgba(0,0,0,0)",
    paper_bgcolor: "rgba(0,0,0,0)",
    
    font: {
        color: "#b2becd"
    }, 
    
    // Axis Title Formatting:
    xaxis: {
        type: 'date',
        tickformat: '%m-%d-%H:%M',
        nticks: 5,
        gridcolor: "#b2becd",
        linewidth: 1,
        mirror: true, 
        showgrid: false 
    },

    yaxis: {                    
        title: "HTTP Requests",
        gridcolor: "#b2becd",
        linewidth: 2,
        mirror: true, 
        showgrid: true

    }

});

// Social Media API App:
const social_media_requests = [{
    type: "scatter",
    name: "GET",
    fill: 'tozeroy', 
    stackgroup: 'one',
    marker: {
        color: '#32CD32'
    },    
    x: app_data['social_media_api']['GET']["Index"].map(date => Date.parse(date)),
    y: app_data['social_media_api']['GET']["Data"]
}, 
{
    type: "scatter",
    name: "POST",
    fill: 'tozeroy', 
    stackgroup: 'one',
    marker: {
        color: '#ff2a26'
      },    
    x: app_data['social_media_api']['POST']["Index"].map(date => Date.parse(date)),
    y: app_data['social_media_api']['POST']["Data"]
}];

Plotly.newPlot("social_media_api_request", social_media_requests, {    
    height: 350,
    margin: {
        t: 40
    },
    title: "Social Media App",
    plot_bgcolor: "rgba(0,0,0,0)",
    paper_bgcolor: "rgba(0,0,0,0)",
    
    font: {
        color: "#b2becd"
    }, 
    
    // Axis Title Formatting:
    xaxis: {
        type: 'date',
        tickformat: '%m-%d-%H:%M',
        nticks: 5,
        gridcolor: "#b2becd",
        linewidth: 1,
        mirror: true, 
        showgrid: false

    },

    yaxis: {
        title: "HTTP Requests",
        gridcolor: "#b2becd",
        linewidth: 1,
        mirror: true, 
        showgrid: true

    }

});

// Finance Data API App:
const finance_requests = [{
    type: "scatter",
    name: "GET",
    fill: 'tozeroy', 
    stackgroup: 'one',
    x: app_data['finance_api']['GET']["Index"].map(date => Date.parse(date)),
    y: app_data['finance_api']['GET']["Data"]
}, 
{
    type: "scatter",
    name: "POST",
    fill: 'tozeroy', 
    stackgroup: 'one',
    x: app_data['finance_api']['POST']["Index"].map(date => Date.parse(date)),
    y: app_data['finance_api']['POST']["Data"]
}];

Plotly.newPlot("finance_api_request", finance_requests, {    
    height: 350,
    title: "Finance App",
    margin: {
        t: 40
    },
    plot_bgcolor: "rgba(0,0,0,0)",
    paper_bgcolor: "rgba(0,0,0,0)",
    
    font: {
        color: "#b2becd"
    }, 
    
    // Axis Title Formatting:
    xaxis: {
        type: 'date',
        tickformat: '%m-%d-%H:%M',
        nticks: 5,
        gridcolor: "#b2becd",
        linewidth: 1,
        mirror: true, 
        showgrid: false

    },

    yaxis: {
        title: "HTTP Requests",
        gridcolor: "#b2becd",
        linewidth: 1,
        mirror: true, 
        showgrid: true

    }

});

// Response Methods Graph:
const response_methods = [{
    type: "scatter",
    name: "200",
    fill: 'tozeroy', 
    stackgroup: 'one',
    x: main_date,
    y: response_codes[200]
}, 
{
    type: "scatter",
    name: "300",
    fill: 'tozeroy', 
    stackgroup: 'one',
    x: main_date,
    y: response_codes[300]
}, 
{
    type: "scatter",
    name: "400",
    fill: 'tozeroy', 
    stackgroup: 'one',
    x: main_date,
    y: response_codes[400]

}, 
{
    type: "scatter",
    name: "500",
    fill: 'tozeroy', 
    stackgroup: 'one',
    x: main_date,
    y: response_codes[500]

}];

// Creating the ScatterPlot for daily request summaries: 
Plotly.newPlot("response_methods", response_methods, {
    
    height: 400,
    title: "Response Codes",
    margin: {
        t: 40
    },
    plot_bgcolor: "rgba(0,0,0,0)",
    paper_bgcolor: "rgba(0,0,0,0)",
    
    font: {
        color: "#b2becd"
    }, 
    
    // Axis Title Formatting:
    xaxis: {
        type: 'date',
        tickformat: '%m-%d-%H:%M',
        nticks: 10,
        gridcolor: "#b2becd",
        linecolor: "#b2becd",
        linewidth: 1,
        mirror: true, 
        showgrid: false
    },

    yaxis: {
        title: "HTTP Requests",
        gridcolor: "#b2becd",
        linecolor: "#b2becd",
        linewidth: 2,
        mirror: true,
        showgrid: false
    }


});
