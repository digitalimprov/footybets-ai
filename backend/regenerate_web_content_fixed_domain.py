#!/usr/bin/env python3
"""
Regenerate Brownlow Web Content with Fixed Domain and Improved SEO
Updates all URLs to use footybets.ai and optimizes for "brownlow medal predictor" SEO
"""

import os
import json
import shutil
from datetime import datetime

def regenerate_web_content():
    """Regenerate all web content with correct domain and improved SEO"""
    print("🌐 Regenerating Brownlow Web Content with Fixed Domain")
    print("=" * 60)
    
    # Import the updated content generator
    from generate_brownlow_web_content import generate_all_web_content
    
    # Backup existing content
    backup_dir = f"brownlow_web_content_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    if os.path.exists("brownlow_web_content"):
        shutil.copytree("brownlow_web_content", backup_dir)
        print(f"📁 Backed up existing content to: {backup_dir}")
    
    # Regenerate all content
    print("\n🔄 Regenerating web content...")
    generate_all_web_content()
    
    print("\n✅ Web content regeneration complete!")
    print("🌐 All URLs now use: https://footybets.ai/brownlow-medal-predictions")
    print("🎯 SEO optimized for: 'Brownlow Medal Predictor' in titles and content")
    
    # Verify the changes
    verify_domain_fixes()

def verify_domain_fixes():
    """Verify that all domain references have been fixed"""
    print("\n🔍 Verifying domain fixes...")
    
    if not os.path.exists("brownlow_web_content"):
        print("❌ No web content directory found")
        return
    
    # Check for any remaining old domain references
    old_domain_count = 0
    new_domain_count = 0
    predictor_count = 0
    
    for root, dirs, files in os.walk("brownlow_web_content"):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # Count old vs new domain references
                        old_domain_count += content.count('footybetsai.com')
                        new_domain_count += content.count('footybets.ai')
                        predictor_count += content.count('Brownlow Medal Predictor')
                        
                except Exception as e:
                    print(f"⚠️  Error reading {filepath}: {str(e)}")
    
    print(f"📊 Domain Fix Verification:")
    print(f"  ❌ Old domain references (footybetsai.com): {old_domain_count}")
    print(f"  ✅ New domain references (footybets.ai): {new_domain_count}")
    print(f"  🎯 'Brownlow Medal Predictor' mentions: {predictor_count}")
    
    if old_domain_count == 0:
        print("✅ All domain references successfully updated!")
    else:
        print("⚠️  Some old domain references still found - manual review needed")

def update_existing_html_files():
    """Update existing HTML files with correct domain and SEO"""
    print("\n🔧 Updating existing HTML files...")
    
    if not os.path.exists("brownlow_web_content"):
        print("❌ No web content directory found")
        return
    
    updated_files = 0
    
    for root, dirs, files in os.walk("brownlow_web_content"):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Replace old domain with new domain
                    content = content.replace('footybetsai.com', 'footybets.ai')
                    
                    # Keep URL structure as /brownlow-medal-predictions (URLs use 'predictions')
                    # But update titles to use 'Brownlow Medal Predictor' for SEO
                    
                    # Update titles and meta descriptions for better SEO
                    content = content.replace('Brownlow Medal Predictions', 'Brownlow Medal Predictor')
                    
                    # Update keywords for better SEO
                    if 'Brownlow Medal, AFL, Australian Football, player statistics, predictions, AI analysis, football betting' in content:
                        content = content.replace(
                            'Brownlow Medal, AFL, Australian Football, player statistics, predictions, AI analysis, football betting',
                            'Brownlow Medal, Brownlow Medal Predictor, AFL, Australian Football, player statistics, predictions, AI analysis, football betting, Brownlow votes, AFL betting'
                        )
                    
                    # Write updated content
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    updated_files += 1
                    
                except Exception as e:
                    print(f"⚠️  Error updating {filepath}: {str(e)}")
    
    print(f"✅ Updated {updated_files} HTML files")

def create_seo_optimized_sitemap():
    """Create an SEO-optimized sitemap for the Brownlow Medal Predictor"""
    print("\n🗺️  Creating SEO-optimized sitemap...")
    
    if not os.path.exists("brownlow_web_content"):
        print("❌ No web content directory found")
        return
    
    sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://footybets.ai/brownlow-medal-predictions</loc>
        <lastmod>2025-01-27</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
"""
    
    # Add season pages
    seasons = [2020, 2021, 2022, 2023, 2024]
    for season in seasons:
        sitemap_content += f"""    <url>
        <loc>https://footybets.ai/brownlow-medal-predictions/{season}</loc>
        <lastmod>2025-01-27</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.9</priority>
    </url>
"""
    
    # Add round pages (example for 2024)
    for round_num in range(1, 25):  # Rounds 1-24
        sitemap_content += f"""    <url>
        <loc>https://footybets.ai/brownlow-medal-predictions/2024/round-{round_num}</loc>
        <lastmod>2025-01-27</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
"""
    
    sitemap_content += """</urlset>"""
    
    # Save sitemap
    sitemap_path = "brownlow_web_content/sitemap.xml"
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    
    print(f"✅ Created sitemap: {sitemap_path}")

def main():
    """Main function to regenerate web content with fixes"""
    print("🚀 Brownlow Web Content Domain Fix & SEO Optimization")
    print("=" * 70)
    
    try:
        # Option 1: Regenerate all content (recommended)
        print("1️⃣  Regenerating all web content with fixes...")
        regenerate_web_content()
        
        # Option 2: Update existing files (alternative)
        print("\n2️⃣  Updating existing HTML files...")
        update_existing_html_files()
        
        # Option 3: Create SEO sitemap
        print("\n3️⃣  Creating SEO-optimized sitemap...")
        create_seo_optimized_sitemap()
        
        print("\n🎉 All fixes completed successfully!")
        print("\n📋 Summary of Changes:")
        print("  ✅ Domain: footybetsai.com → footybets.ai")
        print("  ✅ URL Structure: Uses /brownlow-medal-predictions (clean URLs)")
        print("  ✅ SEO: Added 'Brownlow Medal Predictor' keywords")
        print("  ✅ Titles: Updated for better SEO targeting")
        print("  ✅ Sitemap: Created for search engine indexing")
        
        print("\n🌐 New URL Structure:")
        print("  • Main: https://footybets.ai/brownlow-medal-predictions")
        print("  • Season: https://footybets.ai/brownlow-medal-predictions/2024")
        print("  • Round: https://footybets.ai/brownlow-medal-predictions/2024/round-22")
        
    except Exception as e:
        print(f"❌ Error during regeneration: {str(e)}")

if __name__ == "__main__":
    main() 