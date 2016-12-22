<#import "/layouts/default.ftl" as layout>
<@layout.defaultLayout>

	<h1>Spring Demo</h1>

	<ul>
		<#list model["persons"] as person>
			<li>Person name: ${person.name}</li>
		</#list>
	</ul>

</@layout.defaultLayout>
