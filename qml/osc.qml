import QtQuick 2.1
import "jbQuick/Charts"
import "jbQuick/Charts/QChartGallery.js" as ChartsData
import "netNodes.js" as NetNodes

import GstMix.NetworkData 1.0



Rectangle {
    id: rectangle
    color: "white"
    width: 500
    height: 200
    Text {
        id: loadingText
        text: "Testing\nupload\nSpeed"
        font.pointSize: 8
        anchors.centerIn: parent
	font.family : "Sans"
        PropertyAnimation {
            id: textAnimation
            target: loadingText
            property: "opacity"
            from: 0.0; to: 1.0; duration: 1000
            easing.type: Easing.InOutElastic; easing.amplitude: 2.0; easing.period: 1.5
            loops: Animation.Infinite
        }
    }
    NetworkDataNodes {
        id: rtmpData
        objectName:"nodes"
    }
    Chart {
    id: chart_line;
    objectName:"chart_line"
    width: parent.width;
    anchors.fill: parent
    height: parent.height;
    chartAnimated: true;
    chartAnimationEasing: Easing.InOutElastic;
    chartAnimationDuration: 2000;
    chartType: Charts.ChartType.LINE;
    Component.onCompleted: {
        textAnimation.start()
        getUpSpeed()
        chartData= {
            id:chartData,
            labels:rtmpData.labels,
                datasets: [{
                        fillColor: "rgba(151,187,205,0.5)",
                        strokeColor: "rgba(151,187,205,1)",
                        pointColor: "rgba(151,187,205,1)",
                        pointStrokeColor: "#ffffff",
                        data: NetNodes.getNodes(rtmpData),
                },]
            
        }   
        }

        function updateLine(){
            chart_line.chartData.datasets[0].data=NetNodes.getNodes(rtmpData)
            chart_line.requestPaint()        
        }

        function getUpSpeed(){
            var upSpeed=0;
            var http = new XMLHttpRequest();
            var startTime, endTime;
            var url = "http://speedtest.aerisnavigo.com/speedtest/upload.php";
            var myData = "d="; // the raw data you will send
            var data_size = 1024*1024;//1MB 	// 1024*2048; //2MB 
            myData += Array(data_size).join("k") // A big data
       
            http.onreadystatechange = function() {
                if(http.readyState == 4 && http.status == 200) {
                    endTime = (new Date()).getTime();
                    ShowData();
                }else{
                    ; 
                }
            }
            http.open("POST", url, true);
            
            http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            http.setRequestHeader("Content-length", (myData).length-2);
            http.setRequestHeader("Connection", "close");
 
            startTime = (new Date()).getTime();
            http.send(myData);
            function ShowData()
            {
                myData=null //free myData memory
                var duration = (endTime - startTime) / 1000;
                var bitsLoaded = data_size * 8;
                var speedKbps = ((bitsLoaded / duration)/1024 ).toFixed(2);
                console.log("speed at "+speedKbps+" kbps")
                var upSpeed = []
                var emptyLabels = []
                for(var i = 0 ; i < 50 ; i++)
                {
                    upSpeed[i]=speedKbps;
                    emptyLabels[i]="";
                }
                        
                chart_line.chartData.datasets[1]=
                {
                        fillColor: "rgba(151,187,205,0)",
                        strokeColor: "#F7464A",
                        pointColor: "rgba(151,187,205,0)",
                        pointStrokeColor: "rgba(151,187,205,0)",
                        data: upSpeed,
                        labels: rtmpData.labels,
                }            
                textAnimation.pause()
                loadingText.opacity=0
                chart_line.requestPaint()
            }
        }    
        
    }
    MouseArea {
        anchors.fill: parent
        onClicked: {
            chart_line.chartData.datasets[0].data=NetNodes.getNodes(rtmpData)
            chart_line.requestPaint()
        }
    }
}
