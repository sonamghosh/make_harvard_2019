declare -a ecg_filenames=("chfdb_chf01_275.pkl"
			  "chfdb_chf13_45590.pkl"
			  "chfdbchf15.pkl"
			  "ltstdb_20221_43.pkl"
			  "ltstdb_20321_240.pkl"
			  "mitdb__100_180.pkl"
			  "qtdbsel102.pkl"
			  "stdb_308_0.pkl"
			  "xmitdb_x108_0.pkl"
			  )

for idx in "${ecg_filenames[@]}"
do
  python3 test.py --data ecg --filename "$idx" --save_fig
done
