{
    if ($4 == 200) {
        if($1 in arr)
        {
        }
        else
        {
            for (i in arr)
            {
                mean = arr[i] / n;
                printf("mean\t%s\t%.2fms\n", i, mean);
            }
            split("", arr)
            n = 0;
        }
        arr[$1] += $6 * 1000;
        n++;
    }
}
