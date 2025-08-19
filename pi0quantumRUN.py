from pi0quantum import initialize_pi0system

ops = initialize_pi0system()
diff = ops['diff1D']
result = diff([0.0, 1.0, 0.0, -1.0, 0.0])
print(result)