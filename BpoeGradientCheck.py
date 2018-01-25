if __name__=="__main__":

    from scipy.optimize import check_grad
    import functions3 as func
    import functions24 as func2
    import setVariables6
    from scipy import optimize


    bnds, x0 = setVariables6.setInitials()
    nvar, neq, nineq, ncon = setVariables6.problemSize()

    # for i in range(len(x0)):
    #     print("i: " + str(i) + ", x0[i]: " + str(x0[i]))

    # print('number of variables:', nvar)
    # print('number of equalities:', neq)
    # print('number of inequalities: ', nineq)
    # print('number of constraints: ', ncon)

    # nnzj = len(func2.g_eq_jac(x0, False)) + len(func2.g_ineq_jac(x0, False))
    # print("nnzj=" + str(nnzj))
    # print("ncon=" + str(ncon) + " = " + str(neq) + " + " + str(nineq))
    # print("nvar * ncon: ", nvar * ncon)  # =len(eval_jac_g(x0, False))

    print("len(func2.g_eq_jac(x0))[10] = " + str( len( func2.g_eq_jac(x0, True)[10, :])) )

    print("len(func2.g_eq(x0)) = " + str(len(func2.g_eq(x0))))
    print(str(func2.g_eq_jac(x0, True).shape))




    ################
    # #additional check
    # num = 748
    # func = lambda x: func2.g_eq(x)[num]
    # funcfunc = lambda x: func2.g_eq_jac(x, True)[num, :]
    # fprime = optimize.approx_fprime(x0, func, 0.0001)
    #
    # fprimefprime = funcfunc(x0)
    # for i in range(len(fprime)):
    #     if abs(fprime[i]-fprimefprime[i]) > 0:
    #         print(str(i) + " " + str(fprime[i]) + " " + str(fprimefprime[i]))
    #
    # print(sum((fprime-fprimefprime)**2))
    ################



    #check gradient of equality constraints
    for i in range(neq):

        err_cons_eq = check_grad(func=lambda x: func2.g_eq(x)[i], grad=lambda x: func2.g_eq_jac(x, True)[i, :],
                            x0=x0)
        if abs(err_cons_eq) > 0.00001:
            print("!!!!!!!i: " + str(i) + " error in eq: " + str(err_cons_eq))
        else:
            if i%10 == 0:
                print("i: " + str(i) + " is fine eq: " + str(err_cons_eq))


    #check gradient of inequality constraints
    for i in range(nineq):#10):
        err_cons_ineq = check_grad(func=lambda x: func2.g_ineq(x)[i], grad=lambda x: func2.g_ineq_jac(x, True)[i, :],
                            x0=x0)
        if abs(err_cons_ineq) > 0.001:
            print("!!!!!!!i: " + str(i) + " error in ineq: " + str(err_cons_ineq))
        else:
            if i%10 == 0:
                print("i: " + str(i) + " is fine ineq: " + str(err_cons_ineq))

    #check gradient of objective function
    err_cons_obj = check_grad(func = func.avg_cost, grad = func.avg_cost_grad,
                            x0 = x0)
    if abs(err_cons_obj) > 0.001:
        print("!!!!!!!: "  + " error in err_cons_obj: " + str(err_cons_obj))
    else:
        print("fine err_cons_obj: " + str(err_cons_obj))
