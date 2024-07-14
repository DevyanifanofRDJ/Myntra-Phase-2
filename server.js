const express=require('express');
const cors=require('cors');
const server=express();

server.use(cors());
server.use(express.json());

let analysisResult={};

server.post('/upload-analysis',(req,res)=>{
	analysisResult=req.body;
	res.status(200).send({
		message:'Analysis result received',
		data:analysisResult
	});
});

server.get('/analysis-result',(req,res)=>{
	res.status(200).json(analysisResult);
});

server.listen(5000,()=>{
	console.log('Server is running onn port 5000');
});

