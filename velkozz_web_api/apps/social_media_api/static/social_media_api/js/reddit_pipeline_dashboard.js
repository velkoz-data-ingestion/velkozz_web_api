// Ingesting Reddit Log data from HTML Template:
const redditLogs = JSON.parse(document.getElementById('daily_logs').textContent);
const numPosts = JSON.parse(document.getElementById('num_posts').textContent);
const topLogs = JSON.parse(document.getElementById('top_logs').textContent);
const hotLogs = JSON.parse(document.getElementById('hot_logs').textContent);
const status_code_200 = JSON.parse(document.getElementById('status_code_200').textContent);
const status_code_400 = JSON.parse(document.getElementById('status_code_400').textContent);

// Creating the data trace for Reddit Log Timeseries:
const redditlogsData = [{
    type: "scatter",
    name: "Reddit Logs",
    fill: "tozeroy",
    stackgroup: "one",
    x: redditLogs["Index"].map(date => Date.parse(date)),
    y: redditLogs["Data"]
}];

// Creating a Plot for total Reddit Log Timeseries:
Plotly.newPlot("reddit_log_timeseries", redditlogsData, {
    
    title: "Reddit Log Events", 
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
        tickformat: '%m-%d-%Y',
        nticks: 10,
        gridcolor: "#b2becd",
        linecolor: "#b2becd",
        linewidth: 1,
        mirror: true, 
        showgrid: false
    },

    yaxis: {
        title: "Posts Ingested",
        gridcolor: "#b2becd",
        linecolor: "#b2becd",
        linewidth: 2,
        mirror: true,
        showgrid: false
    }
});

// Data Trace for Num of Posts ingested by the second:
const numPostsData = [{
    type: "scatter",
    name: "posts",
    fill: "tozeroy",
    marker: {
        color: "#ff2a26"
    },
    stackgroup: "one",
    x: numPosts["Index"].map(date => Date.parse(date)),
    y: numPosts["Data"]
}];

// Plot for Num Posts:
Plotly.newPlot("num_posts_timeseries", numPostsData, {
    
    title: "Reddit Posts Ingested", 
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
        tickformat: '%m-%d-%Y:-%H-%M',
        nticks: 10,
        gridcolor: "#b2becd",
        linecolor: "#b2becd",
        linewidth: 1,
        mirror: true, 
        showgrid: false
    },

    yaxis: {
        title: "Posts Ingested",
        gridcolor: "#b2becd",
        linecolor: "#b2becd",
        linewidth: 2,
        mirror: true,
        showgrid: false
    }
});

// Data Trace for Top and Hot Logs:
const topPosts = [{
    type: "scatter",
    name: "Top",
    fill: "tozeroy",
    marker: {
        color: '#ca32cd'
    },    
    stackgroup: "one",
    x: topLogs["Index"].map(date => Date.parse(date)),
    y: topLogs["Data"]
}];
const hotPosts = [{
    type: "scatter",
    name: "Hot",
    fill: "tozeroy",
    marker: {
        color: "#8232cd"
    },
    stackgroup: "one",
    x: hotLogs["Index"].map(date => Date.parse(date)),
    y: hotLogs["Data"],
}];

// Creating a Plot for Hot Reddit Log Timeseries:
Plotly.newPlot('reddit_top_timeseries', topPosts, {
    title: "Top Reddit Posts", 
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
        tickformat: '%m-%d-%Y',
        nticks: 10,
        gridcolor: "#b2becd",
        linecolor: "#b2becd",
        linewidth: 1,
        mirror: true, 
        showgrid: false
    },

    yaxis: {
        title: "Posts Ingested",
        gridcolor: "#b2becd",
        linecolor: "#b2becd",
        linewidth: 2,
        mirror: true,
        showgrid: false
    },

});

Plotly.newPlot('reddit_hot_timeseries', hotPosts, {
    title: "Hot Reddit Posts", 
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
        tickformat: '%m-%d-%Y',
        nticks: 10,
        gridcolor: "#b2becd",
        linecolor: "#b2becd",
        linewidth: 1,
        mirror: true, 
        showgrid: false
    },

    yaxis: {
        title: "Posts Ingested",
        gridcolor: "#b2becd",
        linecolor: "#b2becd",
        linewidth: 2,
        mirror: true,
        showgrid: false
    }
});

// Data Trace for status 200 codes and status 400 codes:
const status_200_trace = {
    type: "scatter",
    name: "200",
    marker: {
        color: "#32CD32"
    },
    fill: "tozeroy",
    stackgroup: "one",
    x: status_code_200["Index"].map(date => Date.parse(date)),
    y: status_code_200["Data"]
};
const status_400_trace = {
    type: "scatter",
    name: "400",
    fill: "tozeroy",
    marker: {
        color: "#ff2a26"
    },
    stackgroup: "one",
    x: status_code_400["Index"].map(date => Date.parse(date)),
    y: status_code_400["Data"]
};

Plotly.newPlot("reddit_post_status", [status_200_trace, status_400_trace], {
    title: "Reddit Post Status", 
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
        tickformat: '%m-%d-%Y',
        nticks: 10,
        gridcolor: "#b2becd",
        linecolor: "#b2becd",
        linewidth: 1,
        mirror: true, 
        showgrid: false
    },

    yaxis: {
        title: "Error Posts",
        gridcolor: "#b2becd",
        linecolor: "#b2becd",
        linewidth: 2,
        mirror: true,
        showgrid: false
    }
});