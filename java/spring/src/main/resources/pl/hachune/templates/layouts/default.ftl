<#macro defaultLayout>
	<!DOCTYPE html>
	<html>
		<head>
			<link href="/static/css/normalize.css" rel="stylesheet"/>
			<link href="/static/css/bootstrap.min.css" rel="stylesheet"/>
		</head>
		<body>
			<div class="container">
				<#nested/>
			</div>
		</body>
	</html>
</#macro>
