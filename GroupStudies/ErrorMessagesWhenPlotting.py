#!/home/oceanw/anaconda3/bin/python
#A mix between the record of the actual error message printed by the Debugger.py
#and code used to plot the errors to investigate where is the mistake from.
import numpy as np
from Will import *
from quat import *
from generalLibrary import *



'''
#These are the error messages I've printed out plotting the grains.
Calculating for frame= 002 / 397
Calculating for frame= 003 / 397
Calculating for frame= 004 / 397
Calculating for frame= 005 / 397
Calculating for frame= 006 / 397
Calculating for frame= 007 / 397
Calculating for frame= 008 / 397
Calculating for frame= 009 / 397
Calculating for frame= 010 / 397
Calculating for frame= 011 / 397
Calculating for frame= 012 / 397
Calculating for frame= 013 / 397
Calculating for frame= 014 / 397
Calculating for frame= 015 / 397
Calculating for frame= 016 / 397
Calculating for frame= 017 / 397
Calculating for frame= 018 / 397
Calculating for frame= 019 / 397
Calculating for frame= 020 / 397
Calculating for frame= 021 / 397
Calculating for frame= 022 / 397
Calculating for frame= 023 / 397
Calculating for frame= 024 / 397
Calculating for frame= 025 / 397
Calculating for frame= 026 / 397
Calculating for frame= 027 / 397
Calculating for frame= 028 / 397
Calculating for frame= 029 / 397
Calculating for frame= 030 / 397
Calculating for frame= 031 / 397
Calculating for frame= 032 / 397
Calculating for frame= 033 / 397
Calculating for frame= 034 / 397
Calculating for frame= 035 / 397
Calculating for frame= 036 / 397
Calculating for frame= 037 / 397
Calculating for frame= 038 / 397
Calculating for frame= 039 / 397
Calculating for frame= 040 / 397
Calculating for frame= 041 / 397
Calculating for frame= 042 / 397
Calculating for frame= 043 / 397
Calculating for frame= 044 / 397
Calculating for frame= 045 / 397
Calculating for frame= 046 / 397
Calculating for frame= 047 / 397
Calculating for frame= 048 / 397
Calculating for frame= 049 / 397
Calculating for frame= 050 / 397
Calculating for frame= 051 / 397
Calculating for frame= 052 / 397
Calculating for frame= 053 / 397
Calculating for frame= 054 / 397
Calculating for frame= 055 / 397
Calculating for frame= 056 / 397
Calculating for frame= 057 / 397
Calculating for frame= 058 / 397
Calculating for frame= 059 / 397
Calculating for frame= 060 / 397
Calculating for frame= 061 / 397
Calculating for frame= 062 / 397
Calculating for frame= 063 / 397
Calculating for frame= 064 / 397
Calculating for frame= 065 / 397
Calculating for frame= 066 / 397
Calculating for frame= 067 / 397
Calculating for frame= 068 / 397
Calculating for frame= 069 / 397
Calculating for frame= 070 / 397
Calculating for frame= 071 / 397
Calculating for frame= 072 / 397
Calculating for frame= 073 / 397
Calculating for frame= 074 / 397
Calculating for frame= 075 / 397
Calculating for frame= 076 / 397
Calculating for frame= 077 / 397
Calculating for frame= 078 / 397
Calculating for frame= 079 / 397
Calculating for frame= 080 / 397
Calculating for frame= 081 / 397
Calculating for frame= 082 / 397
Calculating for frame= 083 / 397
Calculating for frame= 084 / 397
Calculating for frame= 085 / 397
Calculating for frame= 086 / 397
Calculating for frame= 087 / 397
Calculating for frame= 088 / 397
Calculating for frame= 089 / 397
Calculating for frame= 090 / 397
Calculating for frame= 091 / 397
Calculating for frame= 092 / 397
Calculating for frame= 093 / 397
Calculating for frame= 094 / 397
Calculating for frame= 095 / 397
Calculating for frame= 096 / 397
Calculating for frame= 097 / 397
Calculating for frame= 098 / 397
Calculating for frame= 099 / 397
Calculating for frame= 100 / 397
Calculating for frame= 101 / 397
Calculating for frame= 102 / 397
Calculating for frame= 103 / 397
Calculating for frame= 104 / 397
Calculating for frame= 105 / 397
Calculating for frame= 106 / 397
Calculating for frame= 107 / 397
Calculating for frame= 108 / 397
Calculating for frame= 109 / 397
Calculating for frame= 110 / 397
Calculating for frame= 111 / 397
Calculating for frame= 112 / 397
Calculating for frame= 113 / 397
Calculating for frame= 114 / 397
Calculating for frame= 115 / 397
Calculating for frame= 116 / 397
Calculating for frame= 117 / 397
Calculating for frame= 118 / 397
Calculating for frame= 119 / 397
Calculating for frame= 120 / 397
Calculating for frame= 121 / 397
Calculating for frame= 122 / 397
Calculating for frame= 123 / 397
Calculating for frame= 124 / 397
Calculating for frame= 125 / 397
Calculating for frame= 126 / 397
Calculating for frame= 127 / 397
Calculating for frame= 128 / 397
Calculating for frame= 129 / 397
Calculating for frame= 130 / 397
Calculating for frame= 131 / 397
Calculating for frame= 132 / 397
Calculating for frame= 133 / 397
Calculating for frame= 134 / 397
Calculating for frame= 135 / 397
Calculating for frame= 136 / 397
Calculating for frame= 137 / 397
Calculating for frame= 138 / 397
Calculating for frame= 139 / 397
Calculating for frame= 140 / 397
Calculating for frame= 141 / 397
Calculating for frame= 142 / 397
Calculating for frame= 143 / 397
Calculating for frame= 144 / 397
Calculating for frame= 145 / 397
Calculating for frame= 146 / 397
Calculating for frame= 147 / 397
Calculating for frame= 148 / 397
Calculating for frame= 149 / 397
Calculating for frame= 150 / 397
Calculating for frame= 151 / 397
Calculating for frame= 152 / 397
Calculating for frame= 153 / 397
Calculating for frame= 154 / 397
Calculating for frame= 155 / 397
Calculating for frame= 156 / 397
Calculating for frame= 157 / 397
Calculating for frame= 158 / 397
Calculating for frame= 159 / 397
Calculating for frame= 160 / 397
Calculating for frame= 161 / 397
Calculating for frame= 162 / 397
Calculating for frame= 163 / 397
Calculating for frame= 164 / 397
Calculating for frame= 165 / 397
Calculating for frame= 166 / 397
Calculating for frame= 167 / 397
Calculating for frame= 168 / 397
Calculating for frame= 169 / 397
Calculating for frame= 170 / 397
Calculating for frame= 171 / 397
Calculating for frame= 172 / 397
Calculating for frame= 173 / 397
Calculating for frame= 174 / 397
Calculating for frame= 175 / 397
Calculating for frame= 176 / 397
Calculating for frame= 177 / 397
Calculating for frame= 178 / 397
Calculating for frame= 179 / 397
Calculating for frame= 180 / 397
Calculating for frame= 181 / 397
Calculating for frame= 182 / 397
Calculating for frame= 183 / 397
Calculating for frame= 184 / 397
Calculating for frame= 185 / 397
Calculating for frame= 186 / 397
Calculating for frame= 187 / 397
Calculating for frame= 188 / 397
Calculating for frame= 189 / 397
Calculating for frame= 190 / 397
Calculating for frame= 191 / 397
Calculating for frame= 192 / 397
Calculating for frame= 193 / 397
Calculating for frame= 194 / 397
Calculating for frame= 195 / 397
Calculating for frame= 196 / 397
Calculating for frame= 197 / 397
Calculating for frame= 198 / 397
Calculating for frame= 199 / 397
Calculating for frame= 200 / 397
Calculating for frame= 201 / 397
Calculating for frame= 202 / 397
Calculating for frame= 203 / 397
Calculating for frame= 204 / 397
Calculating for frame= 205 / 397
Calculating for frame= 206 / 397
Calculating for frame= 207 / 397
Calculating for frame= 208 / 397
Calculating for frame= 209 / 397
Calculating for frame= 210 / 397
Calculating for frame= 211 / 397
Calculating for frame= 212 / 397
Calculating for frame= 213 / 397
Calculating for frame= 214 / 397
Calculating for frame= 215 / 397
Anomaly detected at grain 52 of frame 215 ! This is because a distance of 2.184 is measured between frames.
Previous frame is plotted at x= 0.2765697887972266 y= -0.007450468796472224 on the polar coordinate system, transformed to xy coordinates.
 Current frame is plotted at x= 0.7982741368203702 y= 2.113007692543183 on the polar coordinate system, transformed to xy coordinates.
Calculating for frame= 216 / 397
Calculating for frame= 217 / 397
Calculating for frame= 218 / 397
Calculating for frame= 219 / 397
Calculating for frame= 220 / 397
Calculating for frame= 221 / 397
Calculating for frame= 222 / 397
Calculating for frame= 223 / 397
Calculating for frame= 224 / 397
Calculating for frame= 225 / 397
Calculating for frame= 226 / 397
Calculating for frame= 227 / 397
Calculating for frame= 228 / 397
Calculating for frame= 229 / 397
Calculating for frame= 230 / 397
Calculating for frame= 231 / 397
Calculating for frame= 232 / 397
Calculating for frame= 233 / 397
Calculating for frame= 234 / 397
Calculating for frame= 235 / 397
Calculating for frame= 236 / 397
Calculating for frame= 237 / 397
Calculating for frame= 238 / 397
Calculating for frame= 239 / 397
Calculating for frame= 240 / 397
Calculating for frame= 241 / 397
Calculating for frame= 242 / 397
Calculating for frame= 243 / 397
Calculating for frame= 244 / 397
Calculating for frame= 245 / 397
Calculating for frame= 246 / 397
Calculating for frame= 247 / 397
Calculating for frame= 248 / 397
Calculating for frame= 249 / 397
Calculating for frame= 250 / 397
Calculating for frame= 251 / 397
Calculating for frame= 252 / 397
Calculating for frame= 253 / 397
Calculating for frame= 254 / 397
Calculating for frame= 255 / 397
Calculating for frame= 256 / 397
Calculating for frame= 257 / 397
Calculating for frame= 258 / 397
Calculating for frame= 259 / 397
Calculating for frame= 260 / 397
Anomaly detected at grain 114 of frame 260 ! This is because a distance of 0.598 is measured between frames.
Previous frame is plotted at x= 0.04867615427934354 y= 0.028035118015727077 on the polar coordinate system, transformed to xy coordinates.
 Current frame is plotted at x= -0.09785008603784565 y= 0.6078943405240438 on the polar coordinate system, transformed to xy coordinates.
Calculating for frame= 261 / 397
Calculating for frame= 262 / 397
Calculating for frame= 263 / 397
Calculating for frame= 264 / 397
Calculating for frame= 265 / 397
Calculating for frame= 266 / 397
Calculating for frame= 267 / 397
Calculating for frame= 268 / 397
Calculating for frame= 269 / 397
Calculating for frame= 270 / 397
Calculating for frame= 271 / 397
Anomaly detected at grain 52 of frame 271 ! This is because a distance of 2.199 is measured between frames.
Previous frame is plotted at x= 0.9368871959819873 y= 2.1147429628543293 on the polar coordinate system, transformed to xy coordinates.
 Current frame is plotted at x= 0.1683140380972569 y= 0.0548344938589934 on the polar coordinate system, transformed to xy coordinates.
Calculating for frame= 272 / 397
Calculating for frame= 273 / 397
Calculating for frame= 274 / 397
Calculating for frame= 275 / 397
Calculating for frame= 276 / 397
Calculating for frame= 277 / 397
Calculating for frame= 278 / 397
Calculating for frame= 279 / 397
Calculating for frame= 280 / 397
Calculating for frame= 281 / 397
Calculating for frame= 282 / 397
Calculating for frame= 283 / 397
Calculating for frame= 284 / 397
Calculating for frame= 285 / 397
Calculating for frame= 286 / 397
Calculating for frame= 287 / 397
Calculating for frame= 288 / 397
Calculating for frame= 289 / 397
Calculating for frame= 290 / 397
Calculating for frame= 291 / 397
Calculating for frame= 292 / 397
Calculating for frame= 293 / 397
Calculating for frame= 294 / 397
Calculating for frame= 295 / 397
Calculating for frame= 296 / 397
Calculating for frame= 297 / 397
Calculating for frame= 298 / 397
Calculating for frame= 299 / 397
Calculating for frame= 300 / 397
Calculating for frame= 301 / 397
Calculating for frame= 302 / 397
Calculating for frame= 303 / 397
Calculating for frame= 304 / 397
Calculating for frame= 305 / 397
Calculating for frame= 306 / 397
Calculating for frame= 307 / 397
Calculating for frame= 308 / 397
Calculating for frame= 309 / 397
Calculating for frame= 310 / 397
Calculating for frame= 311 / 397
Calculating for frame= 312 / 397
Calculating for frame= 313 / 397
Calculating for frame= 314 / 397
Calculating for frame= 315 / 397
Calculating for frame= 316 / 397
Calculating for frame= 317 / 397
Calculating for frame= 318 / 397
Calculating for frame= 319 / 397
Calculating for frame= 320 / 397
Calculating for frame= 321 / 397
Calculating for frame= 322 / 397
Calculating for frame= 323 / 397
Calculating for frame= 324 / 397
Calculating for frame= 325 / 397
Calculating for frame= 326 / 397
Calculating for frame= 327 / 397
Calculating for frame= 328 / 397
Calculating for frame= 329 / 397
Calculating for frame= 330 / 397
Calculating for frame= 331 / 397
Calculating for frame= 332 / 397
Calculating for frame= 333 / 397
Calculating for frame= 334 / 397
Calculating for frame= 335 / 397
Calculating for frame= 336 / 397
Calculating for frame= 337 / 397
Calculating for frame= 338 / 397
Calculating for frame= 339 / 397
Calculating for frame= 340 / 397
Calculating for frame= 341 / 397
Calculating for frame= 342 / 397
Calculating for frame= 343 / 397
Calculating for frame= 344 / 397
Calculating for frame= 345 / 397
Calculating for frame= 346 / 397
Calculating for frame= 347 / 397
Calculating for frame= 348 / 397
Calculating for frame= 349 / 397
Calculating for frame= 350 / 397
Calculating for frame= 351 / 397
Calculating for frame= 352 / 397
Calculating for frame= 353 / 397
Calculating for frame= 354 / 397
Calculating for frame= 355 / 397
Calculating for frame= 356 / 397
Calculating for frame= 357 / 397
Calculating for frame= 358 / 397
Calculating for frame= 359 / 397
Calculating for frame= 360 / 397
Calculating for frame= 361 / 397
Calculating for frame= 362 / 397
Calculating for frame= 363 / 397
Calculating for frame= 364 / 397
Calculating for frame= 365 / 397
Calculating for frame= 366 / 397
Calculating for frame= 367 / 397
Calculating for frame= 368 / 397
Calculating for frame= 369 / 397
Anomaly detected at grain 114 of frame 369 ! This is because a distance of 0.520 is measured between frames.
Previous frame is plotted at x= -0.1279600455595194 y= 0.5217821734466477 on the polar coordinate system, transformed to xy coordinates.
 Current frame is plotted at x= -0.027247407067412154 y= 0.012120398002656472 on the polar coordinate system, transformed to xy coordinates.
Calculating for frame= 370 / 397
Calculating for frame= 371 / 397
Calculating for frame= 372 / 397
Calculating for frame= 373 / 397
Calculating for frame= 374 / 397
Calculating for frame= 375 / 397
Calculating for frame= 376 / 397
Calculating for frame= 377 / 397
Calculating for frame= 378 / 397
Calculating for frame= 379 / 397
Calculating for frame= 380 / 397
Calculating for frame= 381 / 397
Calculating for frame= 382 / 397
Calculating for frame= 383 / 397
Calculating for frame= 384 / 397
Calculating for frame= 385 / 397
Calculating for frame= 386 / 397
Calculating for frame= 387 / 397
Calculating for frame= 388 / 397
Calculating for frame= 389 / 397
Calculating for frame= 390 / 397
Calculating for frame= 391 / 397
Calculating for frame= 392 / 397
Calculating for frame= 393 / 397
Calculating for frame= 394 / 397
Calculating for frame= 395 / 397
Calculating for frame= 396 / 397
Calculating for frame= 397 / 397
'''
#Conclusion: grain 52 and 114 were misbehaving, and giving errors at frame (215,271) and (260,369) respectively.
#The matrices in question are:
R = []
#for grain 52, from
R.append(
[[-0.787184505148,-0.341087251353,-0.513809343842],
[-0.477807561797,-0.189450681721,0.857792733173],
[-0.389923696054,0.920743137992,-0.0138414267888]]
)
#to
R.append(
[[0.606997507728,-0.750398362787,-0.261641592142],
[0.443276581229,0.592957005509,-0.672240925675],
[0.659590705018,0.292068976005,0.69255744535]]
)
#and from 
R.append(
[[0.531181619599,-0.794209977844,-0.295087441435],
[0.461840637916,0.56341050199,-0.685034182663],
[0.710316346545,0.227594194434,0.666071745753]]
)
#to
R.append(
[[-0.833369927098,-0.446046736625,-0.326399867271],
[-0.232858948652,-0.252232219387,0.939231397226],
[-0.501269662598,0.858732330968,0.106336772142]]
)

#for grain 114, from
R.append(
[[-0.99520551281,-0.0121672763225,-0.0970460955367],
[0.0975722427623,-0.054970237756,-0.993709177981],
[0.00675608720775,-0.99841385725,0.0558938720944]]
)
#to
R.append(
[[0.987592764214,-0.0672607504567,0.141903218854],
[0.124904175815,0.884143361296,-0.450210465826],
[-0.0951812951012,0.46234890302,0.881574734744]]
)
#and from
R.append(
[[0.974819886318,-0.101414088911,0.198598519153],
[0.196760954684,0.810272827774,-0.55203538952],
[-0.104934817631,0.577211509882,0.80982439881]]
)
#to
R.append(
[[-0.99575092868,0.0742676124448,0.054446393579],
[-0.0560836644023,-0.0201396320877,-0.998222929914],
[-0.0730391033572,-0.997034962758,0.0242192572069]]
)
#And the reason why this happens is straightfoward:
#We can see with the program below:
#if __name__=="__main__":
if False:
	for n in range(len(R)):
		if n>>2&0x1:	print("Grain 52")
		else:		print("Grain 114")
		#if n>>1&0x1:	print("")
		#else:		print("")
		if    n&0x1:	print(" After discontinuity")
		else:		print("Before discontinuity")
		q = RotToQuat(R[n])
		QuatToRotation(q)

#And the code above prints the following message
'''
Grain 114
Before discontinuity
 	 Rotation by
	 theta = 174.4064076071869 degrees
	 axis [ 0.32291665 -0.63549613 -0.70133409]
 After discontinuity
 	 Rotation by
	 theta = 63.49627600529682 degrees
	 axis [ 0.53877759 -0.51470934  0.66692803]

Before discontinuity
 	 Rotation by
	 theta = 67.64575509489788 degrees
	 axis [ 0.49339262 -0.54354962  0.67905636]
 After discontinuity
 	 Rotation by
	 theta = 171.7425366903598 degrees
	 axis [-0.28024721  0.60878683  0.74218602]

Grain 52
Before discontinuity
 	 Rotation by
	 theta = 175.66635981044445 degrees
	 axis [-0.03113035 -0.68684769  0.72613439]
 After discontinuity
 	 Rotation by
	 theta = 28.758495215253696 degrees
	 axis [0.94837227 0.24638877 0.19970633]

Before discontinuity
 	 Rotation by
	 theta = 37.11190687384814 degrees
	 axis [0.93577733 0.25153013 0.24708985]
 After discontinuity
 	 Rotation by
	 theta = 174.7692739274885 degrees
	 axis [ 0.00651536  0.69918947 -0.71490673]
'''
#if __name__=="__main__":
if False:
	Axes = [
	[ 0.32291665, -0.63549613, -0.70133409],
	[ 0.53877759, -0.51470934,  0.66692803],
	[ 0.49339262, -0.54354962,  0.67905636],
	[-0.28024721,  0.60878683,  0.74218602],
	[-0.03113035, -0.68684769,  0.72613439],
	[0.94837227, 0.24638877, 0.19970633],
	[0.93577733, 0.25153013, 0.24708985],
	[ 0.00651536,  0.69918947, -0.71490673]]

	for axis in Axes:
		print(np.rad2deg(cartesian_spherical(axis[0], axis[1], axis[2])))
	print("Or in multiples of pi:")
	for axis in Axes:
		print(cartesian_spherical(axis[0], axis[1], axis[2])/np.pi)

#whichi gives the following list of axes:
'''
[134.53413646 -63.06336679]
[ 48.16959086 -43.69123265]
[ 47.23005238 -47.76924424]
[ 42.08203463 114.71837301]
[ 43.43670231 267.40492999]
[78.48021346 14.56357573]
[75.69462893 15.0450833 ]
[135.63555587  89.46610777]

#Or in multiples of pi:
[ 0.74741187 -0.35035204]
[ 0.26760884 -0.24272907]#Nearly a 90 degrees (0.480*pi) upwards tilt
[ 0.26238918 -0.26538469]
[0.23378908 0.63732429]#Nearly 1pi change in phi. (0.90)
[0.24131501 1.48558294]
[0.43600119 0.08090875]#Cluless! 0.194 change in theta, 1.40 change in phi.
[0.42052572 0.0835838 ]
[0.75353087 0.49703393]#0.333 change in theta, 0.413 change in phi.
'''
#accompanied by a rotation theta as stated below:
np.array([0.96892449, 0.35275709, 0.37580975, 0.9541252 , 0.97592422, 0.15976942, 0.20617726, 0.97094041]) #in terms of multiples of pi
