{
    if ($4 == 200) {

        if($1 in arr)
        {
        }
        else
        {
            for (i in arr)
            {
                n = asort(arr[i])
                n = int(n * 0.95)
                v = arr[i][n]
                # print(n)
                printf("95%%\t%s\t%.2fms\n", i, v)
            }
            split("", arr)
            n = 0
        }
        arr[$1][n++] = $6 * 1000
    }
}
