# openai-finetune-cls
Finetune Azure OpenAI models (or directly OpenAI models) for a multiclass classification task

## Notes on data preparation for fine tuting

!openai tools fine_tunes.prepare_data -f preproc_ds.jsonl -q

- More than a third of your `completion` column/key is uppercase. Uppercase completions tends to perform worse than a mixture of case encountered in normal language. We recommend to lower case the data if that makes sense in your domain. See https://platform.openai.com/docs/guides/fine-tuning/preparing-your-dataset for more details
- Your data does not contain a common separator at the end of your prompts. Having a separator string appended to the end of the prompt makes it clearer to the fine-tuned model where the completion should begin. See https://platform.openai.com/docs/guides/fine-tuning/preparing-your-dataset for more detail and examples. If you intend to do open-ended generation, then you should leave the prompts empty
- The completion should start with a whitespace character (` `). This tends to produce better results due to the tokenization we use. See https://platform.openai.com/docs/guides/fine-tuning/preparing-your-dataset for more details

Based on the analysis we will perform the following actions:# - [Recommended] Remove 116818 duplicate rows [Y/n]: Y       
- [Recommended] Lowercase all your data in column/key `completion` [Y/n]: Y
c:\CREDEM\venvs\emilio\lib\site-packages\openai\validators.py:452: SettingWithCopyWarning:
A value is trying to be set on a copy of a slice from a DataFrame.
Try using .loc[row_indexer,col_indexer] = value instead

See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
  x[column] = x[column].str.lower()
- [Recommended] Add a suffix separator `\n\n###\n\n` to all prompts [Y/n]: Y
c:\CREDEM\venvs\emilio\lib\site-packages\openai\validators.py:226: SettingWithCopyWarning:
A value is trying to be set on a copy of a slice from a DataFrame.
Try using .loc[row_indexer,col_indexer] = value instead

See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
  x["prompt"] += suffix
- [Recommended] Add a whitespace character to the beginning of the completion [Y/n]: Y
c:\CREDEM\venvs\emilio\lib\site-packages\openai\validators.py:425: SettingWithCopyWarning: 
A value is trying to be set on a copy of a slice from a DataFrame.
Try using .loc[row_indexer,col_indexer] = value instead

See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
  x["completion"] = x["completion"].apply(
- [Recommended] Would you like to split into training and validation set? [Y/n]: Y

Your data will be written to a new JSONL file. Proceed [Y/n]: Y

Wrote modified files to `20230706_preproc_ds_prepared_train.jsonl` and `20230706_preproc_ds_prepared_valid.jsonl`
Feel free to take a look!

Now use that file when fine-tuning:
> openai api fine_tunes.create -t "20230706_preproc_ds_prepared_train.jsonl" -v "20230706_preproc_ds_prepared_valid.jsonl" --compute_classification_metrics --classification_n_classes 271

After you’ve fine-tuned a model, remember that your prompt has to end with the indicator string `\n\n###\n\n` for the model to start generating completions, rather than continuing with the prompt.
Once your model starts training, it'll approximately take 1.96 days to train a `curie` model, and less for `ada` and `babbage`. Queue will approximately take half an hour per job ahead of you.
