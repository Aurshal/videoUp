# videoUp
## All api works with form data

### To run the application:
Create a virtual environment and run following commands.
```python
pip install -r requirements.txt
python app.py
```
### To see the working of upload api:
```
localhost:5000/upload
```
### To get all upload videos:
```
localhost:5000/videos
```
### Charges api:
```
localhost:5000/charges
```
Charges api takes `type`, `size` and `duration` as form data

### Filter video:
```
localhost:5000/videos_by_filter
```
It only implements range of size and range of duration.
You need to provide `min_size`, `max_size` and `min_duration`, `max_duration` as form data.
