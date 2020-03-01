def orientation(S,D,stv,n):
	Orient=[]
	d = stv.dimension()+1
	E = [list(i) for i in S.n_faces(1)]
	#print(d)
	#SD = S.generated_subcomplex(sym(list(D.vertices()),n))
	SD = induced_subcomplex(S,sym(list(D.vertices()),n),d)
	#print("Enters while")
	while len(E)>0:          
		e=E[0]
		#print(list(D.vertices())+list(stv.vertices()))
		#print(list(SD.vertices())+sym(list(stv.vertices()),n))
		#print(e[0] in list(D.vertices())+list(stv.vertices()))
		#print(e[1] in list(SD.vertices())+sym(list(stv.vertices()),n))
		#print(sorted(sym(e,n)) in E)
		if e[0] in list(D.vertices())+list(stv.vertices()) and e[1] in list(SD.vertices())+sym(list(stv.vertices()),n):                                                        
			Orient.append([e,-1])                                              
			if sorted(sym(e,n)) in E:                                                   
				Orient.append([sym(e,n), 1])                                   
				E.remove(sorted(sym(e,n)))  
				E.remove(e)                                           
		if e[1] in list(D.vertices())+list(stv.vertices()) and e[0] in list(SD.vertices())+sym(list(stv.vertices()),n): 				
			Orient.append([e,1])
			if sorted(sym(e,n)) in E:                                                   
				Orient.append([sym(e,n), -1])                               
				E.remove(sorted(sym(e,n))) 
				E.remove(e)                                               
		if contains(e,list(D.vertices())+list(stv.vertices())): 
			if e[0]<e[1]:                           
				Orient.append([e,1]) 
				Orient.append([sym(e,n), -1])
			if e[1]<e[0]:
				Orient.append([e,-1]) 	
				Orient.append([sym(e,n), 1])  
			if sorted(sym(e,n)) in E: 
				E.remove(sorted(sym(e,n))) 				
				#if e[0]<e[1]:                                                  
				#	Orient.append([sym(e,n), -1])
				#if e[1]<e[0]:	                 
				#	Orient.append([sym(e,n), 1]) 	                 			
			E.remove(e) 
		if contains(e,list(SD.vertices())+sym(list(stv.vertices()),n)):
			E.remove(e) 	
	#print("Exit while")		
	#print(Orient)
	return Orient   
	
         
def sym(f, n):
	newf=[]
	for i in f:
		if i<=int(n/2):
			newf.append(i+int(n/2))
		if i>int(n/2):
			newf.append(i-int(n/2))
	return newf		

def contains(small, big):
	c=0
	for i in small:
		if i not in big:
			c=1
	if c==1:		
		return False
	return True
	

def prism(S, B, D, stv, n):
	print("Generating_Sigma")
	O = orientation(S,D,stv,n)
	d = stv.dimension()+1
	E=[]
	for o in O:
		if o[1]==1:
			E.append(["U"+str(o[0][0]),"D"+str(o[0][1])])
		if o[1]==-1:
			E.append(["U"+str(o[0][1]),"D"+str(o[0][0])])	
	#### vertical edges		
	for v in list(S.vertices()):
		E.append(["U"+str(v),"D"+str(v)])	
	for e in list(S.n_faces(1)):
		E.append(["U"+str(e[0]),"U"+str(e[1])])
		E.append(["D"+str(e[0]),"D"+str(e[1])])
	G = Graph(E)
	#print("Start clique complex")
	Sigma=G.clique_complex()
	#print("End clique complex")
	#print(Sigma.automorphism_group())
	#print("Sigma_homology="+str(Sigma.homology()))
	print("Generating_Phi'")
	F = Sigma.facets()
	UB = ["U"+str(i) for i in B.vertices()]
	DB = ["D"+str(i) for i in sym(list(B.vertices()),n)]
	#print len(UB),len(DB)
	#FP = Sigma.generated_subcomplex(UB).join(SimplicialComplex([["P1"]]),rename_vertices=False).facets()
	#FM = Sigma.generated_subcomplex(DB).join(SimplicialComplex([["M1"]]),rename_vertices=False).facets()	
	FP = induced_subcomplex(Sigma,UB,d).join(SimplicialComplex([["P1"]]),rename_vertices=False).facets()
	FM = induced_subcomplex(Sigma,DB,d).join(SimplicialComplex([["M1"]]),rename_vertices=False).facets()	
	SigmaI=SimplicialComplex(Sigma.facets()+FP+FM)
	#print("SigmaI")
	#print SigmaI.homology()
	BSigma=boundary_complex(SigmaI)
	#print BSigma
	FNEW=[]
	for f in BSigma:
		if f[-1][0]=="U" or f[-2][0]=="U":
			FNEW.append(["P2"]+list(f))
		if f[-1][0]=="D" or f[-2][0]=="D":	
			FNEW.append(["M2"]+list(f))
	X=SimplicialComplex(list(SigmaI.facets())+FNEW)	
	#print("Here")	
	return X

def update(Snew, B, D, stv, n):
	d = stv.dimension()+1
	#V1=[i for i in Snew.vertices() if (eval(i[1:]) in D.vertices() or eval(i[1:]) in stv.vertices() or eval(i[1:]) in sym(list(D.vertices()),n)) and i[0]=="U"]	
	#V2=[i for i in Snew.vertices() if (eval(i[1:]) in sym(list(D.vertices()),n) or eval(i[1:]) in sym(list(stv.vertices()),n)) and i[0]=="D"]
	V1=[i for i in Snew.vertices() if (eval(i[1:]) in D.vertices() or eval(i[1:]) in sym(list(stv.vertices()),n) or eval(i[1:]) in sym(list(D.vertices()),n)) and i[0]=="U"]	
	V2=[i for i in Snew.vertices() if eval(i[1:]) in stv.vertices() and i[0]=="D"]
	#Gamma = Snew.generated_subcomplex(V1+V2)
	Gamma = induced_subcomplex(Snew,V1+V2,d)
	#print("Gamma_f_vector="+str(Gamma.f_vector()))	
	#print("Gamma_vertices="+str(Gamma.n_faces(1)))	
	#Bn = Snew.generated_subcomplex(list(Gamma.vertices())+[i for i in Snew.vertices() if i[0]=="U" or i[0]=="P"])
	Bn = induced_subcomplex(Snew,list(Gamma.vertices())+[i for i in Snew.vertices() if i[0]=="U" or i[0]=="P"],d+1)
	MapVertices=[["P1","M1"],["P2","M2"]]
	for i in Snew.vertices():
		if i[0]!="P" and i[0]!="M":
			if eval(i[1:]) in D.vertices():
				MapVertices.append([i,"U"+str(sym([eval(i[1:])],n)[0])])
			if eval(i[1:]) in stv.vertices() or eval(i[1:]) in sym(list(stv.vertices()),n):	
				if i[0]=="U":
					MapVertices.append([i,"D"+str(sym([eval(i[1:])],n)[0])])							
	R = relabel(Snew, len(Snew.vertices()), MapVertices)		
	##star Assumes that P1 is always mapped to 1
	#Y=Snew.link(["P1","U1"]).join(SimplicialComplex([["U1"]]), rename_vertices=False)
	Y=Gamma.star(["U1"])
	#Y2=SimplicialComplex(Snew.generated_subcomplex(["U"+str(i[1:]) for i in Gamma.star(["U1"]).vertices()]))
	#return [relabel_complex(Snew,R),relabel_complex(Bn,R), relabel_complex(Snew.generated_subcomplex(["P1","P2"]+["U"+str(i) for i in list(stv.vertices())]),R), relabel_complex(Snew.star(["P1"]),R),relabel_complex(Y,R),len(Snew.vertices())]
	return [relabel_complex(Snew,R),relabel_complex(Bn,R), relabel_complex(induced_subcomplex(Snew, ["P1","P2"]+["U"+str(i) for i in list(stv.vertices())], d+1),R),relabel_complex(Y,R),len(Snew.vertices())]
	
def boundary_complex(simp_comp):
	d=simp_comp.dimension()
	fac=list(set(simp_comp.facets()))
	r=list(simp_comp.n_faces(d-1))
	b=[]
	for i in range(len(r)):
		f=[]
		n=0
		for j in range(len(fac)):
			if r[i].is_face(fac[j]):
				n=n+1
		if n==1:
			b.append(r[i])	
	return b		

def contract(Sn, D, n):
	print("Contracting_edges_of_Phi'")
	A = deepcopy(Sn)
	for i in D.vertices():
		A = edge_contraction(A, ["U"+str(i),"D"+str(i)])
	for i in sym(list(D.vertices()),n):
		A = edge_contraction(A, ["U"+str(i),"D"+str(i)])
	print("Contracted")	
	return A

def spherePhi(S, B, D, stv, n):
	P=prism(S, B, D, stv, n)
	X=contract(P,D,n)
	#print "Dimension="+str(X.dimension())
	#print "f-vector="+str(X.f_vector())
	#print "Pseudomanifold="+str(X.is_pseudomanifold())
	#print "Homology="+str(X.homology())
	return X

def edge_contraction(S, e):
	V = SimplicialComplex([]).vertices()
	k = 0
	if e[1] in V:
		k = 1
	F = S.facets()
	NF = []
	for f in F:
		if set(e).issubset(set(f)) == False:
			if k == 0:
				if set([e[1]]).issubset(set(f)):
					NF.append(set(f)-set([e[1]])|set([e[0]]))
				else:
					NF.append(set(f))
			if k == 1:
				if set([e[0]]).issubset(set(f)):
					NF.append(set(f)-set([e[0]])|set([e[1]]))
				else:
					NF.append(set(f))
	return SimplicialComplex(NF) 	

def relabel(S, n, Map):
	i=1
	Newmap={}
	for v in Map:
		Newmap[v[0]]=i
		Newmap[v[1]]=sym([i],n)[0]
		i=i+1
	return Newmap	

def relabel_complex(S,Map):
	F = [[Map[i] for i in list(f)] for f in S.facets()]
	return SimplicialComplex(F)

def quotient(S,n):
	F = S.facets()
	QF=[]
	for f in F:
		nf=[]
		for i in f:
			if i > n/2:
				nf.append(i-int(n/2))
			if i <= n/2:	
				nf.append(i)
		QF.append(nf)	
	return SimplicialComplex(QF)

### generated subcomplex given that the subcomplex is pure of dimension d
def induced_subcomplex(S,V,d):
	NF=[list(i) for i in S.n_faces(d) if contains(list(i),V)==True]
	return SimplicialComplex(NF)
		
				


def generate_spheres_up_to_dim_k(k):
	Si=SimplicialComplex([[1,2],[2,3],[3,4],[4,5],[5,6],[1,6]])
	Bi=SimplicialComplex([[1,2],[2,3],[1,6]])
	Di=SimplicialComplex([[1,2]])
	stvi=SimplicialComplex([[3]])
	ni=6
	Sd=[Si]
	RPd=[quotient(Si,ni)]
	print("Triangulation_of_RP"+str(1)+"_saved")
	for j in range(2,k+1):
		Silet=spherePhi(Si,Bi,Di,stvi,ni)
		Ui=update(Silet,Bi,Di,stvi,ni)
		Si = Ui[0]
		Bi=Ui[1]
		Di=Ui[2]
		stvi=Ui[3]
		ni=Ui[4]
		Sd.append(Si)
		RPd.append(quotient(Si,ni))
		print("Triangulation_of_RP"+str(j)+"_saved")
	return Sd, RPd	


	
		
