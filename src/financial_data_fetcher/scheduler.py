import schedule
import time
import logging
from datetime import datetime
from financial_data_fetcher import FinancialDataFetcher
import config

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('financial_data_scheduler.log'),
        logging.StreamHandler()
    ]
)

class FinancialDataScheduler:
    """
    Lớp để lên lịch cập nhật dữ liệu tài chính định kỳ
    """
    
    def __init__(self):
        self.fetcher = FinancialDataFetcher()
        self.logger = logging.getLogger(__name__)
    
    def fetch_and_log_data(self):
        """Lấy dữ liệu và ghi log"""
        try:
            self.logger.info("Starting data fetch...")
            data = self.fetcher.fetch_all_data()
            
            # Log một số thông tin quan trọng
            if 'precious_metals' in data:
                metals = data['precious_metals']
                if 'gold' in metals and 'current_price' in metals['gold']:
                    self.logger.info(f"Gold price: ${metals['gold']['current_price']:.2f}")
                if 'silver' in metals and 'current_price' in metals['silver']:
                    self.logger.info(f"Silver price: ${metals['silver']['current_price']:.2f}")
            
            if 'stock_indices' in data:
                indices = data['stock_indices']
                if 'dow_jones' in indices and 'current_price' in indices['dow_jones']:
                    self.logger.info(f"Dow Jones: {indices['dow_jones']['current_price']:,.2f}")
                if 'vn_index' in indices and 'current_price' in indices['vn_index']:
                    self.logger.info(f"VN Index: {indices['vn_index']['current_price']:,.2f}")
            
            if 'fx' in data:
                fx = data['fx']
                if 'usd_vnd' in fx and 'current_price' in fx['usd_vnd']:
                    self.logger.info(f"USD/VND: {fx['usd_vnd']['current_price']:,.0f}")
            
            self.logger.info("Data fetch completed successfully")
            
        except Exception as e:
            self.logger.error(f"Error fetching data: {str(e)}")
    
    def setup_schedules(self):
        """Thiết lập lịch cập nhật dữ liệu"""
        
        # Cập nhật mỗi 5 phút trong giờ giao dịch
        schedule.every(5).minutes.do(self.fetch_and_log_data)
        
        # Cập nhật mỗi giờ
        schedule.every().hour.do(self.fetch_and_log_data)
        
        # Cập nhật đặc biệt vào đầu ngày
        schedule.every().day.at("09:00").do(self.fetch_and_log_data)
        schedule.every().day.at("12:00").do(self.fetch_and_log_data)
        schedule.every().day.at("18:00").do(self.fetch_and_log_data)
        
        # Cập nhật cuối tuần
        schedule.every().sunday.at("10:00").do(self.fetch_and_log_data)
        
        self.logger.info("Schedules set up successfully")
    
    def run(self):
        """Chạy scheduler"""
        self.logger.info("Starting Financial Data Scheduler...")
        
        # Thiết lập lịch
        self.setup_schedules()
        
        # Lấy dữ liệu ngay lập tức
        self.fetch_and_log_data()
        
        # Chạy scheduler
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("Scheduler stopped by user")
        except Exception as e:
            self.logger.error(f"Scheduler error: {str(e)}")

def run_scheduler():
    """Hàm chạy scheduler"""
    scheduler = FinancialDataScheduler()
    scheduler.run()

if __name__ == "__main__":
    run_scheduler()
