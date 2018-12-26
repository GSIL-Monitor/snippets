a = %{SELECT * FROM subtasks
WHERE
substop != 0 AND
check_status = 1
}

print a
