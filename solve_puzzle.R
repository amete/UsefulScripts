# https://www.linkedin.com/jobs/view/254833965/?refId=3134700481488796373853&trk=d_flagship3_search_srp_jobs
solve_puzzle <- function (n,m,experiments=10000) {
    # n : number of lights
    # m : number of times to use the magic wand
    time.of.travels <- numeric()
    # Conduct a series experiments - can set the seed for reproducibility
    for(i in 1:experiments) {
        x <- sample(0:80,n,replace = TRUE)              # sample n traffic lights randomly
        sort(x)                                         # sort in ascending order
        x <- x[1:(length(x)-m)]                         # remove the ones w/ the magic wand optimally
        time.of.travels <- c(time.of.travels,sum(x))    # calculate the time of waiting
    }
    # Total time of waiting - Round to seconds
    result <- round(mean(time.of.travels)) 
    # Print the result
    print(paste("Calvin will wait approximately",result,"seconds..."))
}
