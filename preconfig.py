import streamlit as st

# ==========================================
# KONFIGURASI HALAMAN & NAMA SISTEM BARU
# ==========================================
st.set_page_config(page_title="SWIGEN", layout="centered", page_icon="⚡")

st.title("⚡ SWIGEN")
st.subheader("Auto-Generator Preconfig Switch")
st.markdown("Portal otomatisasi *script* konfigurasi perangkat distribusi (Raisecom, BDCOM, Fiberhome, Huawei S2700, H3C) agar lebih *sat-set* dan bebas *typo*.")
st.markdown("---")

# ==========================================
# PILIHAN VENDOR UTAMA
# ==========================================
tipe_switch = st.selectbox("Pilih Vendor Perangkat (Switch)", ["Raisecom", "BDCOM", "Fiberhome", "Huawei S2700", "H3C"])
ada_mikrotik = st.radio("Apakah ada perangkat Mikrotik Pelanggan setelah Switch ini?", ["Tidak", "Ya"], horizontal=True)

st.markdown("---")

# ==========================================
# 1. RAISECOM
# ==========================================
if tipe_switch == "Raisecom":
    st.subheader("⚙️ Parameter Raisecom")
    with st.form("form_raisecom"):
        hostname = st.text_input("Hostname", placeholder="Contoh: SBT-INDOMARCO.TGPN-ISCOM2600-CPE-01")
        
        col1, col2, col3 = st.columns(3)
        vlan_nms = col1.text_input("VLAN NMS", placeholder="Contoh: 13")
        vlan_service = col2.text_input("VLAN Service", placeholder="Contoh: 2807")
        desc_vlan_service = col3.text_input("Deskripsi VLAN Service", placeholder="Contoh: INET.BB")
        
        col4, col5 = st.columns(2)
        ip_vlan_nms = col4.text_input("IP Address VLAN NMS", placeholder="Contoh: 172.28.189.126/30")
        ip_route_static = col5.text_input("IP Route Static", placeholder="Contoh: 172.28.189.125")
        
        st.markdown("**Deskripsi Interface**")
        desc_ge1 = st.text_input("Deskripsi ge 1/0/1 (Arah Pelanggan)", placeholder="Contoh: 221405000035 IBBC PT Indomarco")
        
        desc_ge2 = ""
        if ada_mikrotik == "Ya":
            desc_ge2 = st.text_input("Deskripsi ge 1/0/2 (Trunk ke Mikrotik)", placeholder="Contoh: Trunk to Mikrotik Pelanggan")
        
        desc_ge9 = st.text_input("Deskripsi ge 1/0/9 (Arah POP / Trunk Uplink)", placeholder="Contoh: trunk to pop SBT-GI.RENGAT")
        
        submit_raisecom = st.form_submit_button("🔧 Generate Script Raisecom", use_container_width=True)

    if submit_raisecom:
        if not (hostname and vlan_nms and vlan_service and desc_vlan_service and ip_vlan_nms and ip_route_static and desc_ge1 and desc_ge9):
            st.error("Semua parameter wajib diisi!")
        elif ada_mikrotik == "Ya" and not desc_ge2:
            st.error("Deskripsi ge 1/0/2 wajib diisi karena menggunakan Mikrotik!")
        else:
            script = f"config\nhostname {hostname}\n"
            script += f"vlan {vlan_nms}\ndescription NMS\nexit\n"
            script += f"vlan {vlan_service}\ndescription {desc_vlan_service}\nexit\n"
            
            if ada_mikrotik == "Ya":
                script += f"vlan 1132\ndescription nms.ms\nexit\n"
                
            script += f"interface vlan {vlan_nms}\nip address {ip_vlan_nms}\nexit\n"
            script += f"ip route-static 0.0.0.0 0.0.0.0 {ip_route_static}\n"
            script += f"username plniconplussumbagteng password plain ic0nplusSumbagt3ng group administrators\n"
            
            script += f"int ge 1/0/1\ndescription {desc_ge1}\nport link-type access\nport default vlan {vlan_service}\nexit\n"
            
            if ada_mikrotik == "Ya":
                script += f"int ge 1/0/2\ndescription {desc_ge2}\nport link-type trunk\nport trunk allow-pass vlan {vlan_nms},{vlan_service},1132\nexit\n"
                vlan_trunk_pop = f"{vlan_nms},{vlan_service},1132"
            else:
                vlan_trunk_pop = f"{vlan_nms},{vlan_service}"
                
            script += f"int ge 1/0/9\ndescription {desc_ge9}\nport link-type trunk\nport trunk allow-pass vlan {vlan_trunk_pop}\nexit\n"
            script += f"save running-config"

            st.session_state['script_aktif'] = script
            st.session_state['file_aktif'] = f"Preconfig_Raisecom_{hostname}.txt"
            st.session_state['vendor_aktif'] = "Raisecom"

    if st.session_state.get('vendor_aktif') == "Raisecom" and 'script_aktif' in st.session_state:
        st.success("✅ Script berhasil di-generate! Silakan copy kode di bawah ini:")
        st.code(st.session_state['script_aktif'], language='bash')
        
        st.download_button(
            label="📥 Download Preconfig Raisecom (.txt)",
            data=st.session_state['script_aktif'],
            file_name=st.session_state['file_aktif'],
            mime="text/plain",
            use_container_width=True
        )

# ==========================================
# 2. BDCOM
# ==========================================
elif tipe_switch == "BDCOM":
    st.subheader("⚙️ Parameter BDCOM")
    with st.form("form_bdcom"):
        hostname = st.text_input("Hostname", placeholder="Contoh: SBT-INTERNETKU-BD.S2510-CPE-01")
        
        col1, col2, col3 = st.columns(3)
        vlan_nms = col1.text_input("VLAN NMS", placeholder="Contoh: 13")
        vlan_service = col2.text_input("VLAN Service", placeholder="Contoh: 2810")
        desc_vlan_service = col3.text_input("Deskripsi VLAN Service", placeholder="Contoh: INET.BB")
        
        col4, col5 = st.columns(2)
        ip_vlan_nms = col4.text_input("IP Address VLAN NMS & Mask", placeholder="Contoh: 172.28.164.44 255.255.255.248")
        ip_route_default = col5.text_input("IP Route Default", placeholder="Contoh: 172.28.164.41")
        
        st.markdown("**Deskripsi Interface**")
        desc_ge1 = st.text_input("Deskripsi gigaEthernet 0/1 (Arah Pelanggan)", placeholder="Contoh: 04000331490 IBBC Internetku")
        
        desc_ge2 = ""
        if ada_mikrotik == "Ya":
            desc_ge2 = st.text_input("Deskripsi gigaEthernet 0/2 (Trunk ke Mikrotik)", placeholder="Contoh: Trunk to Mikrotik")
        
        desc_ge9 = st.text_input("Deskripsi gigaEthernet 0/9 (Arah POP / Trunk Uplink)", placeholder="Contoh: trunk to SBT-PASIR.PANGARAIAN")
        
        submit_bdcom = st.form_submit_button("🔧 Generate Script BDCOM", use_container_width=True)

    if submit_bdcom:
        if not (hostname and vlan_nms and vlan_service and desc_vlan_service and ip_vlan_nms and ip_route_default and desc_ge1 and desc_ge9):
            st.error("Semua parameter wajib diisi!")
        elif ada_mikrotik == "Ya" and not desc_ge2:
            st.error("Deskripsi gigaEthernet 0/2 wajib diisi karena menggunakan Mikrotik!")
        else:
            script = f"enable\nconfig \nhostname {hostname}\n"
            script += f"username plniconplussumbagteng password ic0nplusSumbagt3ng\n"
            script += f"vlan {vlan_nms}\nname NMS\nexit\n"
            script += f"vlan {vlan_service}\nname {desc_vlan_service}\nexit\n"
            
            if ada_mikrotik == "Ya":
                script += f"vlan 1132\nname nms.ms\nexit\n"
                
            script += f"interface vlan {vlan_nms}\nip address {ip_vlan_nms}\nexit \n"
            script += f"ip route default {ip_route_default} \n"
            
            script += f"interface gigaEthernet 0/1\ndescription {desc_ge1}\nswitchport mode access\nswitchport pvid {vlan_service}\nexit\n"
            
            if ada_mikrotik == "Ya":
                script += f"interface gigaEthernet 0/2\ndescription {desc_ge2}\nswitchport mode trunk\nexit\n"
                
            script += f"interface gigaEthernet 0/9\ndescription {desc_ge9}\nswitchport mode trunk\nexit\n"
            script += f"exit \nwrite"

            st.session_state['script_aktif'] = script
            st.session_state['file_aktif'] = f"Preconfig_BDCOM_{hostname}.txt"
            st.session_state['vendor_aktif'] = "BDCOM"

    if st.session_state.get('vendor_aktif') == "BDCOM" and 'script_aktif' in st.session_state:
        st.success("✅ Script berhasil di-generate! Silakan copy kode di bawah ini:")
        st.code(st.session_state['script_aktif'], language='bash')
        
        st.download_button(
            label="📥 Download Preconfig BDCOM (.txt)",
            data=st.session_state['script_aktif'],
            file_name=st.session_state['file_aktif'],
            mime="text/plain",
            use_container_width=True
        )

# ==========================================
# 3. FIBERHOME
# ==========================================
elif tipe_switch == "Fiberhome":
    st.subheader("⚙️ Parameter Fiberhome")
    with st.form("form_fiberhome"):
        hostname = st.text_input("Hostname", placeholder="Contoh: SBT-SMKN1.PERHENTIAN.RAJA-FH.S4800-CPE-01")
        
        col1, col2, col3 = st.columns(3)
        vlan_nms = col1.text_input("VLAN NMS", placeholder="Contoh: 13")
        vlan_service = col2.text_input("VLAN Service", placeholder="Contoh: 2809")
        desc_vlan_service = col3.text_input("Deskripsi VLAN Service", placeholder="Contoh: INET.BB")
        
        col4, col5 = st.columns(2)
        ip_vlan_nms = col4.text_input("IP Address VLAN NMS", placeholder="Contoh: 172.28.171.174/27")
        ip_route_static = col5.text_input("IP Route Static / Gateway", placeholder="Contoh: 172.28.171.161")
        
        st.markdown("**Deskripsi (Alias) Interface**")
        desc_ge1 = st.text_input("Alias gi 1/0/1 (Arah Pelanggan)", placeholder="Contoh: 221401001435 IBBC SMKN 1")
        
        desc_ge2 = ""
        if ada_mikrotik == "Ya":
            desc_ge2 = st.text_input("Alias gi 1/0/2 (Trunk ke Mikrotik)", placeholder="Contoh: Trunk to Mikrotik")
        
        desc_ge9 = st.text_input("Alias gi 1/0/9 (Arah POP / Trunk Uplink)", placeholder="Contoh: SBT-PLN.RAYONSIMPANGTIGA Port9")
        
        submit_fiberhome = st.form_submit_button("🔧 Generate Script Fiberhome", use_container_width=True)

    if submit_fiberhome:
        if not (hostname and vlan_nms and vlan_service and desc_vlan_service and ip_vlan_nms and ip_route_static and desc_ge1 and desc_ge9):
            st.error("Semua parameter wajib diisi!")
        elif ada_mikrotik == "Ya" and not desc_ge2:
            st.error("Alias gi 1/0/2 wajib diisi karena menggunakan Mikrotik!")
        else:
            script = f"config\nhostname {hostname}\n"
            script += f"vlan {vlan_nms}\nalias NMS\nexit\n"
            script += f"vlan {vlan_service}\nalias {desc_vlan_service}\nexit\n"
            
            if ada_mikrotik == "Ya":
                script += f"vlan 1132\nalias nms.ms\nexit\n"
                
            script += f"interface vlan {vlan_nms}\nip address {ip_vlan_nms}\nexit\n"
            script += f"interface gi 1/0/1\nalias \"{desc_ge1}\"\nport link-type access\nport default vlan {vlan_service}\nexit\n"
            
            if ada_mikrotik == "Ya":
                script += f"interface gi 1/0/2\nalias \"{desc_ge2}\"\nport link-type trunk\nport trunk allow-pass vlan {vlan_nms},{vlan_service},1132\nexit\n"
                vlan_trunk_pop = f"{vlan_nms},{vlan_service},1132"
            else:
                vlan_trunk_pop = f"{vlan_nms},{vlan_service}"
                
            script += f"interface gi 1/0/9\nalias \"{desc_ge9}\"\nport link-type trunk\nport trunk allow-pass vlan {vlan_trunk_pop}\nexit\n\n"
            script += f"ip route-static 0.0.0.0 0.0.0.0 {ip_route_static}\n\n"
            
            tambahan_fiberhome = f"""end

header login "============================================================%. This system is the property of PT Indonesia Comnets Plus .%============================================================%"

username plniconplussumbagteng group administrators password ic0nplusSumbagt3ng 
aaa
 tacacs-server server1 ip-address 10.14.4.19 key iC0N-IPmpls+
 tacacs-server server2 ip-address 10.14.4.12 key iC0N-IPmpls+
 server-group grup1 tacacs-server server1
 server-group grup2 tacacs-server server2
 aaa authentication login method auten1 server-group grup1 local 
 aaa authentication login method auten2 server-group grup2 local 
 aaa authorization method otorisasi1 server-group grup1
 aaa authorization method otorisasi2 server-group grup2
 aaa account login method akunt1 server-group grup1
 aaa account login method akunt2 server-group grup2

line console 1
 timeout 5 0
line vty 1 5
 timeout 5 0
 login authentication aaa method auten1 
 login account aaa method akunt1
 login authorization aaa method otorisasi1
ntp
 ntp unicast-server 10.14.4.2
 ntp unicast-server 10.14.4.23

snmp version all
snmp location {hostname}
snmp community IPMPLS-ICON+ rw
snmp trap-server 10.14.3.12 IPMPLS-ICON+ v2 

syslog server 10.14.4.15

sshd
exit
wr file
y"""
            script += tambahan_fiberhome

            st.session_state['script_aktif'] = script
            st.session_state['file_aktif'] = f"Preconfig_Fiberhome_{hostname}.txt"
            st.session_state['vendor_aktif'] = "Fiberhome"

    if st.session_state.get('vendor_aktif') == "Fiberhome" and 'script_aktif' in st.session_state:
        st.success("✅ Script berhasil di-generate! Silakan copy kode di bawah ini:")
        st.code(st.session_state['script_aktif'], language='bash')
        
        st.download_button(
            label="📥 Download Preconfig Fiberhome (.txt)",
            data=st.session_state['script_aktif'],
            file_name=st.session_state['file_aktif'],
            mime="text/plain",
            use_container_width=True
        )

# ==========================================
# 4. HUAWEI S2700
# ==========================================
elif tipe_switch == "Huawei S2700":
    st.subheader("⚙️ Parameter Huawei S2700")
    with st.form("form_huawei"):
        hostname = st.text_input("Hostname", placeholder="Contoh: SBT-INDOMARCO.T54O-HUAWEI.S2700-CPE-01")
        
        col1, col2, col3 = st.columns(3)
        vlan_nms = col1.text_input("VLAN NMS", placeholder="Contoh: 13")
        vlan_service = col2.text_input("VLAN Service", placeholder="Contoh: 2807")
        desc_vlan_service = col3.text_input("Deskripsi VLAN Service", placeholder="Contoh: IBBC")
        
        col4, col5 = st.columns(2)
        ip_vlan_nms = col4.text_input("IP Address & Mask VLAN NMS", placeholder="Contoh: 172.28.184.251 255.255.255.248")
        ip_route_static = col5.text_input("IP Route Static (Gateway)", placeholder="Contoh: 172.28.184.249")
        
        st.markdown("**Deskripsi Interface**")
        desc_e1 = st.text_input("Deskripsi Ethernet 0/0/1 (Arah Pelanggan)", placeholder="Contoh: 221405000034 ICL Indomarco")
        
        desc_e2 = ""
        if ada_mikrotik == "Ya":
            desc_e2 = st.text_input("Deskripsi Ethernet 0/0/2 (Trunk ke Mikrotik)", placeholder="Contoh: Trunk to Mikrotik")
        
        desc_ge1 = st.text_input("Deskripsi GigabitEthernet 0/0/1 (Arah POP / Trunk Uplink)", placeholder="Contoh: trunk to SBT-ULP.BANGKINANG...")
        
        submit_huawei = st.form_submit_button("🔧 Generate Script Huawei S2700", use_container_width=True)

    if submit_huawei:
        if not (hostname and vlan_nms and vlan_service and desc_vlan_service and ip_vlan_nms and ip_route_static and desc_e1 and desc_ge1):
            st.error("Semua parameter wajib diisi!")
        elif ada_mikrotik == "Ya" and not desc_e2:
            st.error("Deskripsi Ethernet 0/0/2 wajib diisi karena menggunakan Mikrotik!")
        else:
            script = f"system-view\n"
            script += f"sysname {hostname}\n"
            script += f"vlan {vlan_nms}\ndescription NMS\nquit\n"
            script += f"vlan {vlan_service}\ndescription {desc_vlan_service}\nquit\n"
            
            if ada_mikrotik == "Ya":
                script += f"vlan 1132\ndescription nms.ms\nquit\n"
                
            script += f"int vlanif {vlan_nms}\n"
            script += f"ip address {ip_vlan_nms}\n"
            script += f"undo shutdown\nquit\n"
            script += f"ip route-static 0.0.0.0 0.0.0.0 {ip_route_static}\n"
            
            script += f"interface Ethernet 0/0/1\n"
            script += f"description {desc_e1}\n"
            script += f"port link-type access\n"
            script += f"port default vlan {vlan_service}\nquit\n"
            
            if ada_mikrotik == "Ya":
                script += f"interface Ethernet 0/0/2\n"
                script += f"description {desc_e2}\n"
                script += f"port link-type trunk\n"
                script += f"port trunk allow-pass vlan {vlan_nms} {vlan_service} 1132\nquit\n"
                vlan_trunk_pop = f"1 {vlan_nms} {vlan_service} 1132"
            else:
                vlan_trunk_pop = f"1 {vlan_nms} {vlan_service}"
                
            script += f"interface GigabitEthernet 0/0/1\n"
            script += f"description {desc_ge1}\n"
            script += f"port link-type trunk\n"
            script += f"port trunk allow-pass vlan {vlan_trunk_pop}\nquit\n"
            
            script += f"aaa\nlocal-user j2m password cipher multimedia123\n"
            script += f"local-user j2m privilege level 15\n"
            script += f"local-user j2m service-type telnet ssh\nquit\n\n"
            
            script += f"user-interface vty 0 4\n"
            script += f" authentication-mode aaa\n"
            script += f" user privilege level 15\n"
            script += f" idle-timeout 30 0\n"

            st.session_state['script_aktif'] = script
            st.session_state['file_aktif'] = f"Preconfig_Huawei_{hostname}.txt"
            st.session_state['vendor_aktif'] = "Huawei"

    if st.session_state.get('vendor_aktif') == "Huawei" and 'script_aktif' in st.session_state:
        st.success("✅ Script berhasil di-generate! Silakan copy kode di bawah ini:")
        st.code(st.session_state['script_aktif'], language='bash')
        
        st.download_button(
            label="📥 Download Preconfig Huawei S2700 (.txt)",
            data=st.session_state['script_aktif'],
            file_name=st.session_state['file_aktif'],
            mime="text/plain",
            use_container_width=True
        )

# ==========================================
# 5. H3C
# ==========================================
elif tipe_switch == "H3C":
    st.subheader("⚙️ Parameter H3C")
    with st.form("form_h3c"):
        hostname = st.text_input("Hostname", placeholder="Contoh: SBT-KLINIK.RS.SEMEN.PADANG-H3C-CPE-01")
        
        col1, col2, col3 = st.columns(3)
        vlan_nms = col1.text_input("VLAN NMS", placeholder="Contoh: 13")
        vlan_service = col2.text_input("VLAN Service", placeholder="Contoh: 2810")
        desc_vlan_service = col3.text_input("Deskripsi VLAN Service", placeholder="Contoh: METRO")
        
        col4, col5 = st.columns(2)
        ip_vlan_nms = col4.text_input("IP Address & Mask VLAN NMS", placeholder="Contoh: 172.28.163.69 255.255.255.224")
        ip_route_static = col5.text_input("IP Route Static (Gateway)", placeholder="Contoh: 172.28.163.65")
        
        st.markdown("**Deskripsi Interface**")
        desc_ge5 = st.text_input("Deskripsi GigabitEthernet1/0/5 (Arah Pelanggan)", placeholder="Contoh: IBBC Klinik RS Semen Padang")
        
        desc_ge6 = ""
        if ada_mikrotik == "Ya":
            desc_ge6 = st.text_input("Deskripsi GigabitEthernet1/0/6 (Trunk ke Mikrotik)", placeholder="Contoh: Trunk to Mikrotik")
        
        desc_ge9 = st.text_input("Deskripsi GigabitEthernet1/0/9 (Arah POP / Trunk Uplink)", placeholder="Contoh: Trunk to SBT-PLN.RKR.ULP...")
        
        submit_h3c = st.form_submit_button("🔧 Generate Script H3C", use_container_width=True)

    if submit_h3c:
        if not (hostname and vlan_nms and vlan_service and desc_vlan_service and ip_vlan_nms and ip_route_static and desc_ge5 and desc_ge9):
            st.error("Semua parameter wajib diisi!")
        elif ada_mikrotik == "Ya" and not desc_ge6:
            st.error("Deskripsi GigabitEthernet1/0/6 wajib diisi karena menggunakan Mikrotik!")
        else:
            script = f"system-view\n"
            script += f"sysname {hostname}\n#\n"
            
            script += f"vlan 1\n#\n"
            script += f"vlan {vlan_nms}\n name NMS\n#\n"
            script += f"vlan {vlan_service}\n name {desc_vlan_service}\n#\n"
            
            if ada_mikrotik == "Ya":
                script += f"vlan 1132\n name nms.ms\n#\n"
                
            script += f"interface Vlan-interface{vlan_nms}\n"
            script += f" ip address {ip_vlan_nms}\n#\n"
            
            script += f"interface GigabitEthernet1/0/5\n"
            script += f" description {desc_ge5}\n"
            script += f" port link-type access\n"
            script += f" port access vlan {vlan_service}\n#\n"
            
            if ada_mikrotik == "Ya":
                script += f"interface GigabitEthernet1/0/6\n"
                script += f" description {desc_ge6}\n"
                script += f" port link-type trunk\n"
                script += f" port trunk permit vlan 1 {vlan_nms} {vlan_service} 1132\n#\n"
                vlan_trunk_pop = f"1 {vlan_nms} {vlan_service} 1132"
            else:
                vlan_trunk_pop = f"1 {vlan_nms} {vlan_service}"
                
            script += f"interface GigabitEthernet1/0/9\n"
            script += f" description {desc_ge9}\n"
            script += f" port link-type trunk\n"
            script += f" port trunk permit vlan {vlan_trunk_pop}\n#\n"
            
            script += f"ip route-static 0.0.0.0 0 {ip_route_static}\n#\n"
            
            tambahan_h3c = """telnet server enable
#
 irf mac-address persistent timer
 irf auto-update enable
 undo irf link-delay
 irf member 1 priority 1
#
 lldp global enable
#
 password-recovery enable
#
 stp global enable
#
line class aux
 user-role network-admin
#
line class vty
 user-role network-operator
#
line aux 0
 user-role network-admin
#
line vty 0 4
 authentication-mode scheme
 user-role network-admin
 user-role network-operator
#
line vty 5 63
 user-role network-operator
#
radius scheme system
 user-name-format without-domain
#
domain system
#
 domain default enable system
#
user-group system
#
local-user j2m class manage
 password hash $h$6$qCbH5KEAFHjIk85L$OLqloKuHN0clUKgrVZOG8bAJTS0iM3pqwirAPfsn3A5HWCCYLzEOhn6kVwgOQkpRXemPC2slULYslik6oygDpg==
 service-type telnet
 authorization-attribute user-role network-admin
 authorization-attribute user-role network-operator
#
return"""
            script += tambahan_h3c

            st.session_state['script_aktif'] = script
            st.session_state['file_aktif'] = f"Preconfig_H3C_{hostname}.txt"
            st.session_state['vendor_aktif'] = "H3C"

    if st.session_state.get('vendor_aktif') == "H3C" and 'script_aktif' in st.session_state:
        st.success("✅ Script berhasil di-generate! Silakan copy kode di bawah ini:")
        st.code(st.session_state['script_aktif'], language='bash')
        
        st.download_button(
            label="📥 Download Preconfig H3C (.txt)",
            data=st.session_state['script_aktif'],
            file_name=st.session_state['file_aktif'],
            mime="text/plain",
            use_container_width=True
        )