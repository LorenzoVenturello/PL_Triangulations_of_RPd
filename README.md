# PL_Triangulations_of_RPd
Supplementary material to https://arxiv.org/abs/1910.07433.

We report a naive implementation of the procedure described in the paper "A new family of triangulations of RP^d", by L. Venturello and H. Zheng.

The code is contained in the file RPd_code.py. It is written in python and has to be executed in sage.

Once the file is loaded, the function "generate_spheres_up_to_dim_k(k)" can be called. It takes an integer k>0 as an argument and it returns two lists.

-The first contains a centrally symmetric PL triangulation of S^i for i=1,...,k without cs invariant 4-cycles. These correspond to the spheres \Phi in https://arxiv.org/abs/1910.07433
-The second list contains the quotients of the complexes in the first list w.r.t. the antipodal symmetry. These simplicial complexes are PL triangulations of the real projective space RP^i for i=1,...,k.

Our result is that the triangulations of RP^i have 1/2(3F_{i-1}+7F_i+3F_{i+1}-4) many vertices, where F_i is the i-th Fibonacci number (F_0=0, F_1=1, F_i=F_{i-1}+F_{i-2}).

The code is still primitive. On our laptop we verified the construction up to dimension 6, before the running time slowed down.

We include the files "Real_projective_spaces.py" and "Real_projective_spaces_f_vectors.py" containing the lists of facets and the f-vectors respectively of the triangulations of RP^i.

The construction is inductive, and it depends on fixing a certain locally acyclic orientation of the graph of the sphere on one dimension lower. Different orientations could give rise to non-isomorphic triangulation. The code implemented here does not leave this choice to the user, but it fixes a standard globally acyclic orientation induced by the labeling of the vertices.

