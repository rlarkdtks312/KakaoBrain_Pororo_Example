from pororo import Pororo
from tqdm.auto import tqdm
import pandas as pd

def pororo_mrc(df, col_name, qst_list, save=False, sfname='mrc_result'):
    mrc = Pororo(task="mrc", lang="ko")
    
    fail_count = 0
    for idx, qst in tqdm(enumerate(qst_list)):
        ans_list = []
        for row in tqdm(list(df[col_name])):
            try:
                ans = mrc(qst,row)
                ans_list.append(ans[0])
            except:
                fail_count += 1
                ans_list.append('Fail')
        df[f'ans{idx+1}'] = ans_list
        
    print(f'성공 : {len(df)*len(qst_list)-fail_count} / 실패 : {fail_count}')
    
    if save == True:
        df.to_csv(f'./{sfname}.csv', encoding='utf-8-sig', index=False)
        
    return df

def pororo_zsl(df, col_name, categories, save=False, sfname='zsl_result'):
    zsl = Pororo(task="zero-topic", lang="ko")
    
    cat_list = []
    fail_count = 0
    for row in tqdm(list(df[col_name])):
        try:
            result = zsl(row, categories)
            max_cat = max(result, key=result.get)
            cat_list.append(max_cat)
        except:
            fail_count += 1
            cat_list.append('Fail')
    df['category'] = cat_list
    
    print(f'성공 : {len(df)-fail_count} / 실패 : {fail_count}')

    if save == True:
        df.to_csv(f'./{sfname}.csv', encoding='utf-8-sig', index=False)
    
    return df

# Optical Character Recognoition
def pororo_ocr(df, img_path_col, save=False, sfname='ocr_result'):
    ocr = Pororo(task="ocr", lang="ko")
    
    dscr_list = []
    bdpl_list = []
    fail_count = 0
    for row in tqdm(list(df[img_path_col])):
        try:
            result = ocr(row, detail=True)
            dscr_list.append(result['description'])
            bdpl_list.append(result['bounding_poly'])
        except:
            dscr_list.append('Fail')
            bdpl_list.append('Fail')
            fail_count += 1
    df['description'] = dscr_list
    df['bounding_poly'] = bdpl_list
    
    print(f'성공 : {len(df)-fail_count} / 실패 : {fail_count}')
    
    if save == True:
        df.to_csv(f'./{sfname}.csv', encoding='utf-8-sig', index=False)
    
    return df

