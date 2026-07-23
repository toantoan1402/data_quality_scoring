import pandas as pd
from faker import Faker
import random
from datetime import timedelta

fake = Faker('vi_VN')

def generate_comprehensive_dirty_data(num_rows=2000):
    data = []
    print(f"⏳ Đang sinh {num_rows} dòng dữ liệu tổng hợp (Khách hàng & Đơn hàng)...")
    
    for i in range(num_rows):
        # ==========================================
        # 1. DỮ LIỆU SẠCH (Hợp lệ 100%)
        # ==========================================
        
        # --- Thông tin cá nhân & Mạng ---
        customer_id = f"KH{i+1:06d}"
        name = fake.name()
        age = random.randint(18, 100)
        phone = random.choice(['098', '090', '084']) + str(random.randint(1000000, 9999999))
        email = fake.ascii_free_email()
        cccd = str(random.randint(100000000000, 999999999999))
        tax_id = str(random.randint(1000000000, 9999999999)) # 10 số
        ipv4_address = fake.ipv4()
        website_url = fake.url()
        
        # --- Thông tin Đơn hàng & Sản phẩm ---
        order_id = f"ORD-{random.randint(10000, 99999)}"
        product_sku = f"{fake.lexify(text='???').upper()}-{random.randint(100, 999)}"
        rating = random.randint(1, 5)
        discount_percent = random.randint(0, 50)
        
        # --- Dữ liệu logic (Cần tính toán để luôn đúng) ---
        start_date = fake.date_between(start_date='-1y', end_date='today')
        end_date = start_date + timedelta(days=random.randint(1, 30)) # end_date > start_date
        
        cost_price = round(random.uniform(10.0, 50.0), 2)
        sale_price = round(cost_price + random.uniform(5.0, 20.0), 2) # sale_price > cost_price
        
        qty_imported = random.randint(50, 200)
        qty_sold = random.randint(1, qty_imported) # qty_imported >= qty_sold

        # ==========================================
        # 2. TIÊM LỖI (Dirty Data)
        # ==========================================
        
        # Lỗi định dạng (Accuracy)
        if random.random() < 0.10: age = random.choice([-5, 150, None])
        if random.random() < 0.10: email = email.replace('@', '')
        if random.random() < 0.10: order_id = str(random.randint(10000, 99999)) # Mất chữ ORD-
        if random.random() < 0.10: rating = random.randint(6, 10) # Vượt quá 5 sao
        if random.random() < 0.10: website_url = "www.sai-dinh-gang" # Thiếu http://
        
        # Lỗi logic chéo (Consistency)
        if random.random() < 0.15: 
            end_date = start_date - timedelta(days=10) # Ngày kết thúc < Ngày bắt đầu
        
        if random.random() < 0.15: 
            sale_price = cost_price - 5.0 # Bán lỗ (Giá bán < Giá gốc)
            
        if random.random() < 0.15: 
            qty_sold = qty_imported + random.randint(10, 50) # Bán nhiều hơn số lượng nhập

        # Lỗi thiếu dữ liệu (Completeness)
        if random.random() < 0.05: name = None
        
        data.append([
            customer_id, name, age, phone, email, cccd, tax_id, ipv4_address, website_url,
            order_id, product_sku, rating, discount_percent, 
            start_date, end_date, cost_price, sale_price, qty_imported, qty_sold
        ])

    columns = [
        'id', 'name', 'age', 'phone_number', 'email', 'cccd', 'tax_id', 'ipv4_address', 'website_url',
        'order_id', 'product_sku', 'rating', 'discount_percent',
        'start_date', 'end_date', 'cost_price', 'sale_price', 'qty_imported', 'qty_sold'
    ]

    df = pd.DataFrame(data, columns=columns)
    
    # Ép kiểu dữ liệu an toàn
    df['age'] = pd.to_numeric(df['age'], errors='coerce')
    
    file_name = "full_dataset_logical_dirty.csv"
    df.to_csv(file_name, index=False, encoding='utf-8')
    
    print(f"✅ Đã tạo thành công file: {file_name}")

if __name__ == "__main__":
    generate_comprehensive_dirty_data(2000)